import keyboard
import time
from datetime import datetime
from macro_maker import globals
from pynput import mouse
from .. import position_translator
import pyautogui

# Keep track of key states to avoid repeated messages

key_states = {}
recorded_data = []
last_event_time = datetime.now()
stop_recording = False

# pynput button name to pyautodui button name
button_layout_lookup = {
    "Button.left": "left",
    "Button.right": "right",
    "Button.middle": "middle",
}


def add_wait():
    """
    Add wait between last entry and this entry
    """
    global last_event_time
    wait_time = (datetime.now() - last_event_time).total_seconds()
    last_event_time = datetime.now()
    entry_buffer = {
        "ActionType": "Wait",
        "Data": wait_time
    }
    if globals.debug:
        print(entry_buffer)
    recorded_data.append(entry_buffer)


def on_click(x, y, button, pressed):
    """
    Record click data
    """
    add_wait()
    global button_layout_lookup
    state = 'down' if pressed else 'up'
    button_name = button_layout_lookup[str(button)]
    px, py = pyautogui.position()
    px, py = position_translator.center_to_global_translation(px, py)
    entry_buffer = {
        "ActionType": "MouseAction",
        "Data": f"({px}, {py}) | ({button_name}, {state})"
    }
    if globals.debug:
        print(entry_buffer)

    recorded_data.append(entry_buffer)


def on_scroll(x, y, dx, dy):
    """
    Record y axis scroll
    """
    add_wait()
    px, py = pyautogui.position()
    px, py = position_translator.center_to_global_translation(px, py)
    entry_buffer = {
        "ActionType": "Scroll",
        "Data": f"({px}, {py}) | {dy}"
    }
    if globals.debug:
        print(entry_buffer)

    recorded_data.append(entry_buffer)


def on_key_event(event):
    """
    Record key press
    """
    key = event.name
    global stop_recording

    if stop_recording or key == globals.recorder_exit_key:
        stop_recording = True
        return

    if key == globals.recorder_breakpoint_key:
        if event.event_type == keyboard.KEY_DOWN:
            # Add key press
            entry_buffer = {
                "ActionType": "Break point",
            }
            if globals.debug:
                print(entry_buffer)
            recorded_data.append(entry_buffer)
        return

    if key_states.get(key) != event.event_type:
        # If there's a state change in key
        key_states[key] = event.event_type
        add_wait()

        # Add key press
        entry_buffer = {
            "ActionType": "KeyDown" if event.event_type == keyboard.KEY_DOWN else "KeyUp",
            "Data": key
        }
        if globals.debug:
            print(entry_buffer)
        recorded_data.append(entry_buffer)

        # Add a small delay to avoid repeated events
        time.sleep(0.2)


def start_recording():
    print("Keyboard listener started. Press 'right alt' to quit.")

    global last_event_time, stop_recording
    last_event_time = datetime.now()
    stop_recording = False

    keyboard.hook(on_key_event)

    mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()

    keyboard.wait(globals.recorder_exit_key)
    mouse_listener.stop()

    print("Recording stopped")
    return recorded_data
