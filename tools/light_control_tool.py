from tools.utils import govee_control

def light_control(state):
    """
    Control the lights in the user's location. If state is "True", turn lights on; if "False", turn off.
    """
    if state == "True":
        govee_control.turn_light(on=True)
    elif state == "False":
        govee_control.turn_light(on=False)
    return f"LIGHT SET: STATE: {state}"

tool_interface = {
    "type": "function",
    "function": {
        "name": "light_control",
        "description": "Control the lights in user's location",
        "parameters": {
            "type": "object",
            "properties": {
                "state": {"type": "string", "enum": ["True", "False"]}
            },
            "required": ["state"]
        }
    }
}

available_functions = {
    "light_control": light_control
} 