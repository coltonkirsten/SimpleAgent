import os
import json
import datetime
import inspect
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Settings file path
SETTINGS_FILE = Path("settings.json")

# Default settings
DEFAULT_SETTINGS = {
    "logging": {
        "print_system_logs": True,
        "print_debug_logs": True,
        "print_error_logs": True,
        "print_llm_logs": True,
        "print_tool_logs": True,
        "write_to_file": True
    }
}

# Load or create settings
def load_settings():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error parsing {SETTINGS_FILE}. Using default settings.")
    
    # Create settings file with defaults
    with open(SETTINGS_FILE, "w") as f:
        json.dump(DEFAULT_SETTINGS, f, indent=4)
    
    return DEFAULT_SETTINGS

# Create a new log file for this session
SESSION_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = logs_dir / f"log_{SESSION_TIMESTAMP}.txt"

# Initialize settings
settings = load_settings()

def log(message, type="system", source=None):
    """
    Log a message.
    
    Args:
        message: The message to log
        type: The type of log (system, debug, error, llm, tool)
    """

    if source is None:
        source = "Unnamed Agent"
    # Get the caller's frame info
    caller_frame = inspect.currentframe().f_back
    source_info = f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno}"
    
    # Determine if we should print this log type
    should_print = False
    if type == "system" and settings["logging"]["print_system_logs"]:
        should_print = True
    elif type == "debug" and settings["logging"]["print_debug_logs"]:
        should_print = True
    elif type == "error" and settings.get("logging", {}).get("print_error_logs", True):
        should_print = True
    elif type == "llm" and settings.get("logging", {}).get("print_llm_logs", True):
        should_print = True
    elif type == "tool" and settings.get("logging", {}).get("print_tool_logs", True):
        should_print = True

    # Format the log message
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_log = f"[{timestamp}] < ({source}) {type}> ({source_info}) {message}"
    
    # Print to console if enabled
    if should_print:
        # Add color to console output
        color_code = "\033[34m" if type == "system" else "\033[36m"  # Blue for system, Cyan for debug
        if type == "error":
            color_code = "\033[31m"  # Red color for errors
        elif type == "llm":
            color_code = "\033[35m"  # Purple/Magenta color for LLM logs
        elif type == "tool":
            color_code = "\033[33m"  # Yellow color for tool logs
        # Only print the last 100 characters of the message
        truncated_message = message[-100:] if len(message) > 100 else message
        print(f"\n{color_code}< ({source}) {type} > {truncated_message}\033[0m")
    
    # Write to log file if enabled
    if settings["logging"]["write_to_file"]:
        with open(LOG_FILE, "a") as f:
            f.write(f"{formatted_log}\n")