import time
import pyautogui
import keyboard
from PIL import ImageGrab

from .. import position_translator
from .. import globals


stop_signal = False


def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN:
        key = event.name
        print(f"Pressed key: {key}")
        if key == globals.execution_panic_key:
            print("Stopping detector")
            global stop_signal
            stop_signal = True
            return


def log_cursor_position():
    """
    Constantly check and log cursor position and the color of the pixel under it
    When a key is pressed, log which key is pressed
    """
    print(f"Logging cursor location and pixel data, press {globals.execution_panic_key} to stop")
    keyboard.hook(on_key_event)
    while not stop_signal:
        # Get the current cursor position
        x, y = pyautogui.position()
        x, y = position_translator.center_to_global_translation(x, y)
        screenshot = ImageGrab.grab(all_screens=True)
        pixel = screenshot.getpixel((x, y))

        print(f"Cursor position: ({x}, {y}) | {pixel}")

        # Wait for 1 second
        time.sleep(1)


if __name__ == "__main__":
    log_cursor_position()
