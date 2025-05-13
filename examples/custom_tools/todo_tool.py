import json
import os

class TodoListTool:
    def __init__(self, storage_file='todos.json'):
        self.storage_file = storage_file
        self.todos = self._load_todos()

    def _load_todos(self):
        """Load todos from file or create an empty list if file doesn't exist."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading todos: {e}")
            return []

    def _save_todos(self):
        """Save todos to file."""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.todos, f)
        except Exception as e:
            print(f"Error saving todos: {e}")

    def add_todo(self, todo):
        """
        Add a new todo to the list.
        
        :param todo: The todo item to add
        :return: Confirmation message
        """
        self.todos.append(todo)
        self._save_todos()
        return f"Todo added: {todo}"

    def remove_todo(self, todo):
        """
        Remove a specific todo from the list.
        
        :param todo: The todo item to remove
        :return: Confirmation message
        """
        if todo in self.todos:
            self.todos.remove(todo)
            self._save_todos()
            return f"Todo removed: {todo}"
        return f"Todo not found: {todo}"

    def show_todos(self):
        """
        Show all existing todos.
        
        :return: List of todos
        """
        return self.todos

# Create a global instance of the TodoListTool
todo_list_tool = TodoListTool()

def add_todo(todo):
    """
    Add a new todo via the tool.
    
    :param todo: Todo item to add
    :return: Confirmation message
    """
    return todo_list_tool.add_todo(todo)

def remove_todo(todo):
    """
    Remove a specific todo via the tool.
    
    :param todo: Todo item to remove
    :return: Confirmation message
    """
    return todo_list_tool.remove_todo(todo)

def show_todos():
    """
    Retrieve all existing todos.
    
    :return: List of todos
    """
    return todo_list_tool.show_todos()

# Tool interface definition
tool_interface = [
    {
        "type": "function",
        "function": {
            "name": "add_todo",
            "description": "Add a new todo item to the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo": {
                        "type": "string",
                        "description": "The todo item to add"
                    }
                },
                "required": ["todo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_todo",
            "description": "Remove a specific todo item from the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo": {
                        "type": "string",
                        "description": "The todo item to remove"
                    }
                },
                "required": ["todo"]
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

# Available functions mapping
available_functions = {
    "add_todo": add_todo,
    "remove_todo": remove_todo,
    "show_todos": show_todos
}