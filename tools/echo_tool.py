def echo(text):
    """
    Echo the input text in lowercase.
    
    Args:
        text (str): The text to be echoed.
    
    Returns:
        str: The input text in lowercase.
    """
    print(text.lower())
    return text.lower()

def echo_louder(text):
    """
    Echo the input text in uppercase.
    
    Args:
        text (str): The text to be echoed loudly.
    
    Returns:
        str: The input text in uppercase.
    """
    print(text.upper())
    return text.upper()

tool_interface = [
    {
        "type": "function",
        "function": {
            "name": "echo",
            "description": "Echo the input text in lowercase",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to echo"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "echo_louder",
            "description": "Echo the input text in uppercase",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to echo loudly"}
                },
                "required": ["text"]
            }
        }
    }
]

available_functions = {
    "echo": echo,
    "echo_louder": echo_louder
}