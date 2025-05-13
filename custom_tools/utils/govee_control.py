#!/usr/bin/env python3

import requests

# Govee API key provided
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.environ.get("GOVEE_API_KEY")
API_ENDPOINT = "https://developer-api.govee.com/v1/devices/control"
DEVICES_ENDPOINT = "https://developer-api.govee.com/v1/devices"

# Get device information from environment variables
DEVICE_ID = os.environ.get("GOVEE_DEVICE_ID")
MODEL = os.environ.get("GOVEE_MODEL")

def send_command(command):
    """
    Sends a command to the Govee device using the provided API key.
    """
    headers = {
        "Content-Type": "application/json",
        "Govee-API-Key": API_KEY
    }
    
    payload = {
        "device": DEVICE_ID,
        "model": MODEL,
        "cmd": command
    }
    
    try:
        # The API requires a PUT request to control the device.
        response = requests.put(API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        # print("Command sent successfully!")
        # print("Response:", response.json())
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        print("Response:", response.text)
    except requests.exceptions.RequestException as err:
        print("Error:", err)

def turn_light(on=True):
    """
    Turns the light on or off.
    """
    state = "on" if on else "off"
    cmd = {
        "name": "turn",
        "value": state
    }
    send_command(cmd)

def set_brightness(brightness):
    """
    Sets the brightness of the light. Brightness should be in the range 0-100.
    """
    try:
        brightness = int(brightness)
        if brightness < 0 or brightness > 100:
            print("Brightness must be between 0 and 100.")
            return
    except ValueError:
        print("Please enter a valid number for brightness.")
        return
    
    cmd = {
        "name": "brightness",
        "value": brightness
    }
    send_command(cmd)

def set_color(r, g, b):
    """
    Sets the light color using RGB values (each should be in the range 0-255).
    """
    try:
        r, g, b = int(r), int(g), int(b)
        for value in (r, g, b):
            if value < 0 or value > 255:
                print("RGB values must be between 0 and 255.")
                return
    except ValueError:
        print("Please enter valid numbers for the RGB values.")
        return
    
    cmd = {
        "name": "color",
        "value": {"r": r, "g": g, "b": b}
    }
    send_command(cmd)

def list_devices():
    """
    Fetches devices registered with your Govee account and prints only the light devices.
    
    It first attempts to extract light devices from 'data.types.light', and if this key is not
    available, it looks inside 'data.devices' and filters for devices that support the 'turn' command.
    """
    headers = {
        "Content-Type": "application/json",
        "Govee-API-Key": API_KEY
    }
    
    try:
        response = requests.get(DEVICES_ENDPOINT, headers=headers)
        response.raise_for_status()
        devices_data = response.json()
        print("\nDevices (Lights):")
        
        light_devices = []
        if "data" in devices_data:
            data = devices_data["data"]
            if isinstance(data, dict):
                if "types" in data and "light" in data["types"]:
                    # Devices are grouped explicitly under types.light
                    light_devices = data["types"]["light"]
                elif "devices" in data:
                    # Fallback: devices are listed directly under data.devices.
                    # We'll filter out devices that support the 'turn' command.
                    for device in data["devices"]:
                        if "turn" in device.get("supportCmds", []):
                            light_devices.append(device)
                else:
                    print("Unexpected data format:", devices_data)
                    return
            elif isinstance(data, list):
                # If 'data' is a list, attempt to filter light devices directly.
                light_devices = [d for d in data if "turn" in d.get("supportCmds", [])]
            else:
                print("Unexpected data format:", devices_data)
                return
            
            print(f"Found {len(light_devices)} light device(s):")
            for device in light_devices:
                print(device)
        else:
            print("Unexpected data format:", devices_data)
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        print("Response:", response.text)
    except requests.exceptions.RequestException as err:
        print("Error:", err)

def main():
    """
    Main interactive function for controlling Govee lights.
    """
    while True:
        print("\nGovee Light Controller")
        print("----------------------")
        print("1. Turn Light On")
        print("2. Turn Light Off")
        print("3. Set Brightness")
        print("4. Set Color (RGB)")
        print("5. List Light Devices")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            turn_light(on=True)
        elif choice == "2":
            turn_light(on=False)
        elif choice == "3":
            brightness = input("Enter brightness level (0-100): ").strip()
            set_brightness(brightness)
        elif choice == "4":
            r_val = input("Enter red value (0-255): ").strip()
            g_val = input("Enter green value (0-255): ").strip()
            b_val = input("Enter blue value (0-255): ").strip()
            set_color(r_val, g_val, b_val)
        elif choice == "5":
            list_devices()
        elif choice == "6":
            print("Exiting the controller.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()