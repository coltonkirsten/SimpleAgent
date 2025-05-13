import importlib

def load_tools(config):
    """
    Load the tools specified in the configuration dictionary.
    Args:
        config (dict): Dictionary containing tool configuration
    Returns:
        list: A two-element list containing:
              - a list of tool interface dictionaries,
              - a dictionary merging available functions from all loaded tools.
    """
    if config is None:
        return None
    
    all_interfaces = []
    merged_functions = {}
    
    for tool_module in config.get("tools", []):
        mod = importlib.import_module(tool_module)
        if hasattr(mod, "tool_interface"):
            if isinstance(mod.tool_interface, list):
                all_interfaces.extend(mod.tool_interface)
            else:
                all_interfaces.append(mod.tool_interface)
        if hasattr(mod, "available_functions"):
            merged_functions.update(mod.available_functions)
    
    return [all_interfaces, merged_functions]