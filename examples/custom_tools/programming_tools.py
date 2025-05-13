import os

def _validate_file_path(filename):
    """
    Helper function to validate file paths against allowed directory.
    Returns the full validated path.
    """
    try:
        with open("current_directory.txt", "r") as f:
            allowed_path = f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("The file 'current_directory.txt' does not exist.")
    
    allowed_path = os.path.abspath(allowed_path)
    full_path = os.path.abspath(filename)
    if not full_path.startswith(allowed_path):
        raise ValueError("Access to the specified file is not allowed.")
    
    return full_path

def write_file(filename, code):
    """
    Create and write code to a new script with the given filename.
    Overwrites if the file already exists.
    """
    full_path = _validate_file_path(filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(code)
    
    print(f"\033[1;94m\n< created new file {filename} >\033[0m")
    return "SUCCESS"

def delete_file(filename):
    """
    Delete a file with the given filename if it exists and is within the allowed directory.
    """
    full_path = _validate_file_path(filename)
    if os.path.exists(full_path):
        os.remove(full_path)
        print(f"\033[1;91m\n< deleted file {filename} >\033[0m")
        return "SUCCESS"
    else:
        raise FileNotFoundError(f"File '{filename}' does not exist.")

### INTERFACE ###
tool_interface = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create and write code to a new script with the given filename. Overwrites if the file already exists.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the new file to be created."
                    },
                    "code": {
                        "type": "string",
                        "description": "The source code to write into the file."
                    }
                },
                "required": ["filename", "code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a file if it exists within the allowed directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to be deleted."
                    }
                },
                "required": ["filename"]
            }
        }
    },
]

available_functions = {
    "write_file": write_file,
    "delete_file": delete_file,
}

programming_tools = [tool_interface, available_functions] 