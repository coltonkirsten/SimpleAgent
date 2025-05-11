from openai import OpenAI
from . import apikey, logger

# history is saved automatically
# messages can be passed in, 
# can assume models passed in are supported by openai

# Features to add
# - set temperature
# - set tools

class OpenAIBackend:
    def __init__(
        self,
        model,
        system_role,
        messages = None,
        reasoning = False,
        save_history = True,
        stream = True
    ):
        # init client
        self.client = OpenAI(api_key=apikey.api_key)
        self.model = model
        self.system_role = system_role
        
        if messages is None:
            self.messages = [{"role": "system", "content": system_role}]
        else:
            self.messages = messages

        # settings
        # TODO add reasoning for supported models
        self.reasoning = reasoning
        self.save_history = save_history
        self.stream = stream

    # TODO determine helper funcs neeeded (set_model, set_messages, forget, etc)

    def _add_user_msg(self, msg):
        self.messages.append({"role": "user", "content": msg})

    def _add_assistant_msg(self, msg):
        self.messages.append({"role": "assistant", "content": msg})

    def show_chat(self):
        return self.messages

    def prompt(self, prompt):
        if not self.save_history:
            self.messages = [{"role": "system", "content": self.system_role}]
        if prompt is not None:
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
            # "temperature": self.temperature,
            # "max_tokens": self.max_tokens,
        }

        response = self.client.chat.completions.create(**request_params)
        logger.log(f"Request Params: {request_params}", "OPENAI API CALL")

        if self.stream:
            return self._stream_handler(response)
        else:
            return self._static_handler(response)

    def _stream_handler(self, response):
        full_response = ""
        for chunk in response:
            logger.log(f"Chunk: {chunk}", "debug")
            delta = chunk.choices[0].delta

            if delta.content is not None:
                full_response += delta.content
                yield delta.content
        
        # After generator is exhausted, save to history
        self._add_assistant_msg(full_response)
                
        

    def _static_handler(self, response):
        content = response.choices[0].message.content
        self._add_assistant_msg(content)
        return content