import os
import sys
from SimpleAgent.litellm_interface import LitellmInterface

def generate_tool_filename(tool_name):
    """Convert a tool name to a valid Python filename."""
    # Convert to snake_case and ensure it ends with _tool.py
    snake_case = ''.join(['_' + c.lower() if c.isupper() else c.lower() for c in tool_name]).lstrip('_')
    if not snake_case.endswith('_tool'):
        snake_case += '_tool'
    return f"{snake_case}.py"

def create_tool(prompt):
    """Use LLM to generate a new tool based on the provided prompt."""
    # System message to instruct the model on how to create a tool
    system_message = """
    You are a tool creation assistant. Your job is to create Python tool modules compatible with the SimpleAgentFramework.
    
    The tool file should include:
    1. All necessary imports
    2. One or more functions that implement the tool's functionality
    3. A `tool_interface` variable that defines the tool's API using JSON Schema
    4. An `available_functions` dictionary that maps function names to their implementations
    
    Follow these guidelines:
    - Make sure function parameters are properly documented in the tool interface
    - Include proper error handling
    - Add appropriate docstrings for functions
    - For complex tools, use logging with the log() function
    - Make the tool implementation realistic and practical
    
    Use this template as a guide:
    ```python
    import [necessary modules]
    
    def tool_function_name(param1, param2):
        '''
        Function docstring explaining what the tool does.
        '''
        # Function implementation
        return result
    
    tool_interface = [
        {
            "type": "function",
            "function": {
                "name": "tool_function_name",
            "description": "Description of what the tool does",
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "Description of param1"},
                    "param2": {"type": "number", "description": "Description of param2"}
                },
                    "required": ["param1", "param2"]
                }
            }
        },
        {
        "type": "function",
        "function": {
            "name": "show_todos",
            "description": "Show all existing todos in the list",
            "parameters": {
                "type": "object",
                "properties": {},
                    "required": []
                }
            }
        }
    ]
    
    available_functions = {
        "tool_function_name": tool_function_name,
        "show_todos": show_todos
    }
    ```
    
    Respond ONLY with the complete Python code for the tool without any additional explanations.
    """
    
    # Initialize LitellmInterface with appropriate model
    bot = LitellmInterface(
        model="openai/gpt-4.1",
        system_role=system_message,
        stream=False
    )
    
    # Get response from the AI
    response = bot.prompt(f"Create a tool that: {prompt}")
    
    # Extract code from the response
    code = response.strip()
    
    # If the response is wrapped in markdown code blocks, remove them
    if code.startswith("```python"):
        code = code.split("```python", 1)[1]
    if code.endswith("```"):
        code = code.rsplit("```", 1)[0]
    
    code = code.strip()
    
    return code

def save_tool(code, tool_name=None):
    """Save the generated tool code to a file in the tools directory."""
    # Extract tool name from the code if not provided
    if tool_name is None:
        # Try to find the tool_interface and extract the name
        for line in code.split('\n'):
            if '"name":' in line:
                potential_name = line.split('"name":', 1)[1].strip()
                if potential_name.startswith('"') and potential_name.endswith('",'):
                    tool_name = potential_name[1:-2]  # Remove quotes and comma
                    break
    
    if tool_name is None:
        tool_name = "custom_tool"  # Default name
    
    # Generate filename
    filename = generate_tool_filename(tool_name)
    
    # Ensure tools directory exists
    tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_tools")
    if not os.path.exists(tools_dir):
        tools_dir = "custom_tools"  # Fall back to relative path
    
    filepath = os.path.join(tools_dir, filename)
    
    # Save the code to file
    with open(filepath, 'w') as f:
        f.write(code)
    
    return filepath

def main():
    print("\n===== Tool Creator Agent =====")
    print("This agent creates new tools for the SimpleAgentFramework based on your prompt.")
    print("Type 'exit', 'quit', or 'bye' to exit.")
    print("=" * 50)
    
    while True:
        # Get user input
        prompt = input("\nDescribe the tool you want to create (or type 'exit' to quit): ")
        
        # Check for exit commands
        if prompt.lower() in ["exit", "quit", "bye"]:
            print("\nGoodbye!")
            break
        
        print("\nGenerating tool... This may take a moment.")
        
        # Generate tool code
        try:
            code = create_tool(prompt)
            filepath = save_tool(code)
            print(f"\nTool created successfully and saved to: {filepath}")
            print("You can now use this tool by adding it to your Tools configuration.")
        except Exception as e:
            print(f"\nError creating tool: {e}")

if __name__ == "__main__":
    main() 