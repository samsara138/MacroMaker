import pyautogui
import time

from macro_maker import globals
from macro_maker.position_translator import center_to_global_translation


# Mouse
def click_on_position(x, y, button="left"):
    hold_on_position(x, y, globals.click_duration, button)


def hold_on_position(x, y, duration=1.0, button="left"):
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown(button=button)
    time.sleep(duration)
    pyautogui.mouseUp(button=button)


def mouse_action(x, y, button="left", down=True):
    pyautogui.moveTo(x, y)
    if down:
        pyautogui.mouseDown(button=button)
    else:
        pyautogui.mouseUp(button=button)


def mouse_drag(start_x, start_y, end_x, end_y, duration):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.dragTo(end_x, end_y, duration=duration)


def mouse_scroll(x, y, magnitude):
    pyautogui.moveTo(x, y)
    pyautogui.scroll(magnitude * globals.scroll_multiplier)


def move_to(x, y, duration):
    pyautogui.moveTo(x, y, duration)


# Keyboard
def type_string(string_to_send):
    print(f"Typing: |{string_to_send}|")
    pyautogui.typewrite(string_to_send)


def press_key(key_name):
    pyautogui.press(key_name)


def hold_key(key_name, down):
    if down:
        pyautogui.keyDown(key_name)
    else:
        pyautogui.keyUp(key_name)
