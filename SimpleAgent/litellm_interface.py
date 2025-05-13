from litellm import completion
from dotenv import load_dotenv
from .utils import logger
from .utils.tool_manager import load_tools
import json

## load environment variables from .env file
load_dotenv()

class LitellmInterface:
    def __init__(
        self,
        model,
        system_role,
        name="Unnamed Agent",
        tools = None,
        messages = None,
        save_history = True,
        stream = True
    ):
        # init client
        self.name = name
        self.model = model
        self.system_role = system_role

        # settings
        self.save_history = save_history
        self.stream = stream

        # load messages
        if messages is None:
            self.messages = [{"role": "system", "content": system_role}]
        else:
            self.messages = messages

        logger.log(f"Agent {self.name} initialized with model {self.model}", "system", self.name)

        # load tools
        self.tools = load_tools(tools) # returns [interfaces, functions], or None if tools=None
        if self.tools:
            logger.log(f"Loaded tool interfaces: {self.tools[0]}", "debug", self.name)
            logger.log(f"Available functions: {list(self.tools[1].keys())}", "system", self.name)
        else:
            logger.log("No tools loaded", "system", self.name)


        # state management
        self.second_response = False
        

    # TODO determine helper funcs neeeded (set_model, set_messages, forget, etc)

    def show_chat(self):
        """Return the chat history in a human-readable format."""
        # Return a formatted version of the messages for better readability
        return json.dumps(self.messages, indent=2, ensure_ascii=False)

    def prompt(self, prompt, image=None):
        if not self.save_history:
            self.messages = [{"role": "system", "content": self.system_role}]
        
        if prompt is not None:
            if image is not None:
                # Create multimodal message with text and image
                content = [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}",
                        },
                    },
                ]
                self._add_user_msg(content)
            else:
                # Standard text-only message
                self._add_user_msg(prompt)
        else:
            logger.log("No user message provided", "error")
            return None
        
        return self._api_call()
    
    def _api_call(self):
        request_params = {
            "model": self.model,
            "messages": self.messages,
            "stream": self.stream,
        }

        if self.tools:
            request_params["tools"] = self.tools[0]
            request_params["tool_choice"] = "auto"

        response = completion(**request_params)
        logger.log(f"LITELLM({self.model}) Request Params: {request_params}", "llm", self.name)

        if self.stream:
            return self._stream_handler(response)
        else:
            return self._static_handler(response)

    def _stream_handler(self, response):
        full_response = ""
        tool_calls = {}  # accumulate tool calls by index
        
        for chunk in response:
            logger.log(f"Chunk: {chunk}", "debug", self.name)
            delta = chunk.choices[0].delta

            # tool branch
            if delta.tool_calls:
                tc = delta.tool_calls[0]
                index = tc.index
                
                # if this is a new tool call index, add it to the dict
                if index not in tool_calls:
                    tool_calls[index] = {
                        "index": index,
                        "type": tc.type,
                        "id": tc.id,
                        "name": tc.function.name,
                        "arguments": tc.function.arguments if tc.function.arguments else ""
                    }
                else:
                    # append to existing tool call arguments
                    if tc.function.arguments:
                        # clean empty args if needed
                        if tool_calls[index]["arguments"] == "{}":
                            tool_calls[index]["arguments"] = ""
                        
                        tool_calls[index]["arguments"] += tc.function.arguments

            if chunk.choices[0].finish_reason == "tool_calls":
                # process all tool calls in order of their indices
                for idx in sorted(tool_calls.keys()):
                    tool_call = tool_calls[idx]
                    self._stream_add_tool_use_msg(tool_call)
                    tool_name = tool_call["name"]
                    tool_args = json.loads(tool_call["arguments"])
                    tool_result = self._call_tool(tool_name, tool_args)
                    self._add_tool_result(tool_call["id"], tool_name, tool_result)
                self.second_response = True
            
            # follow up response from llm after tool call
            if self.second_response:
                self.second_response = False
                yield from self._api_call()
    
            # content branch
            if delta.content is not None:
                full_response += delta.content
                yield delta.content
        
        # After generator is exhausted, save to history
        self._add_assistant_msg(full_response)

    def _static_handler(self, response):
        response_msg = response.choices[0].message
        content = response_msg.content
        tool_calls = response_msg.tool_calls

        if tool_calls:
            self.second_response = True
            for tool_call in tool_calls:
                self._add_tool_use_msg(tool_call)
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                tool_result = self._call_tool(tool_name, tool_args)
                self._add_tool_result(tool_call.id, tool_name, tool_result)
        if self.second_response:
            self.second_response = False
            final_response = self._api_call()
            return final_response
        else:
            self._add_assistant_msg(content)
            return content
    
    def _call_tool(self, name, args):
        tools = self.tools[1]
        if name not in tools:
            logger.log(f"Tool '{name}' not found", "error", self.name)
            return f"No tool named {name} available."
        try:
            res = tools[name](**args)
            logger.log(f"{name}({args}) -> {res}", "tool", self.name)
            return str(res)
        except Exception as exc:
            logger.log(f"{name}({args}) -> ERROR", "tool", self.name)
            logger.log(f"TOOL ERROR: {name}: {exc}", "error", self.name)
            return f"Error with tool {name}: {exc}"
        
    def _add_user_msg(self, msg):
        self.messages.append({"role": "user", "content": msg})

    def _add_assistant_msg(self, msg):
        self.messages.append({"role": "assistant", "content": msg})

    def _add_tool_use_msg(self, tool_call):
        tool_use_msg = {
            "role": "assistant",
            "tool_calls": [{
                "id": tool_call.id,
                "type": tool_call.type,
                "index": tool_call.index,
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                }
            }]
        }
        self.messages.append(tool_use_msg)

    def _stream_add_tool_use_msg(self, tool_call):
        tool_use_msg = {
            "role": "assistant",
            "tool_calls": [{
                "id": tool_call["id"],
                "type": tool_call["type"],
                "index": tool_call["index"],
                "function": {
                    "name": tool_call["name"],
                    "arguments": tool_call["arguments"]
                }
            }]
        }
        self.messages.append(tool_use_msg)


    def _add_tool_result(self, tool_call_id, function_name, function_response):
        self.messages.append(
          {
              "role": "tool",
              "tool_call_id": tool_call_id,
              "name": function_name,
              "content": function_response,
          }
        )