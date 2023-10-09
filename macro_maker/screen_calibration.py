import keyboard
import pyautogui
import json
from . import globals


def start_calibration():
    """
    Calculate offset produced by pyautogui
    The top left corner should be (0, 0), but pyautogui might now follow that system
    """
    print("First, move your mouse to the left most of your screen(s), then press Enter")
    keyboard.wait("Enter")
    x, _ = pyautogui.position()
    print("Now, move your mouse to the up most of your screen(s), then press Enter")
    keyboard.wait("Enter")
    _, y = pyautogui.position()
    globals.x_offset = x
    globals.y_offset = y

    file_path = "config.json"
    with open(file_path, 'r') as file:
        data = json.load(file)

    data["Calibration"] = {
        "XOffset": globals.x_offset,
        "YOffset": globals.y_offset
    }

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Calibration complete, your offset is {x, y}, this has been written to your config file")
