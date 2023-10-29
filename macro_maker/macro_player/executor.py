import math
from PIL import ImageGrab
from macro_maker import position_translator, globals
from . import action
import time
import random
from datetime import datetime
import keyboard

panic = False


def parse_int(value):
    return int(value)


def parse_float(value):
    return float(value)


def euclidean_distance(color1, color2):
    """
    Calculate the similarity of 2 colors
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    distance = math.sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)
    return distance


def parse_tuple(tuple_string):
    t = tuple_string.strip('()').split(',')
    return t[0], t[1]


def parse_float_tuple(tuple_string):
    t0, t1 = parse_tuple(tuple_string)
    return parse_float(t0), parse_float(t1)


def parse_jump_point(tuple_string):
    t0, t1 = parse_tuple(tuple_string)
    return t0, parse_int(t1)


def parse_mouse_pos_tuple(tuple_string):
    """
    Parse pos tuple and translate to center position for pyautogui
    """
    x, y = parse_float_tuple(tuple_string)
    x, y = position_translator.global_to_center_translation(x, y)
    return x, y


def parse_color_triple(triple_string):
    color_data = triple_string.strip('()').split(',')
    return list(map(parse_int, color_data))


def parse_drag_data(data):
    data = data.split("|")
    start_x, start_y = parse_mouse_pos_tuple(data[0])
    end_x, end_y = parse_mouse_pos_tuple(data[1])
    duration = parse_float(data[2])
    return start_x, start_y, end_x, end_y, duration


def parse_scroll_data(data):
    data = data.split("|")
    x, y = parse_mouse_pos_tuple(data[0])
    scroll_amount = parse_int(data[1])
    return x, y, scroll_amount


def parse_move_to_data(data):
    data = data.split("|")
    x, y = parse_mouse_pos_tuple(data[0])
    scroll_amount = parse_int(data[1])
    return x, y, scroll_amount


def parse_trigger_data(data):
    data = data.split("|")
    x, y = parse_tuple(data[0])
    color_data = parse_color_triple(data[1])
    if len(data) > 2:
        wait_duration = parse_float(data[2])
    else:
        wait_duration = -1
    return parse_int(x), parse_int(y), [color_data[0], color_data[1], color_data[2]], wait_duration


def parse_branch_trigger_data(data):
    data = data.split("|")
    x, y = parse_tuple(data[0])
    color_data = parse_color_triple(data[1])
    true_jump_point = data[2]
    false_jump_point = data[3]
    return parse_int(x), parse_int(y), color_data, true_jump_point, false_jump_point


def parse_mouse_action(data):
    data = data.split("|")
    x, y = parse_mouse_pos_tuple(data[0])
    button_value = [value.strip() for value in data[1].strip('()').split(',')]
    return x, y, button_value[0], button_value[1]


def record_jump_points(data):
    """
    Record and parse all the jump point and jump entry
    """
    jump_points = {}
    jump_counters = {}
    for i in range(len(data)):
        entry = data[i]
        if entry["ActionType"] == "JumpPoint":
            print_log(f"Jump point found: {entry}")
            if entry["Data"] in jump_points:
                print(f"Fatal Error: repeated jump point {entry['Data']}, abort")
                exit(10)
            jump_points[entry["Data"]] = i + 1
        elif entry["ActionType"] == "Jump":
            print_log(f"Jump found: {entry}")
            try:
                jump_data = parse_tuple(entry["Data"])
                # jump location to jump destination, jump counter and default value
                jump_counters[i] = [jump_data[0], parse_int(jump_data[1]), parse_int(jump_data[1])]
            except IndexError:
                jump_data = entry["Data"]
                # Infinite jump
                jump_counters[i] = [jump_data, -1, -1]
    return jump_points, jump_counters


def on_key_event(event):
    """
    Listen to panic button
    """
    key = event.name
    if str(key) == globals.execution_panic_key and event.event_type == keyboard.KEY_DOWN:
        print("Panic! macro will stop asap")
        global panic
        panic = True


def execute_macro(macro):
    index = 0
    jump_points, jump_counter = record_jump_points(macro)

    print_log(f"Jump points: {jump_points}")
    print_log(f"Jump counters: {jump_counter}")

    # Panic button trigger
    keyboard.hook(on_key_event)

    while index < len(macro):
        if panic:
            panic_action()
        entry = macro[index]

        print_log(f"Entry {index}: {entry}")
        action_type = entry["ActionType"].strip()

        if entry["Data"]:
            action_data = entry["Data"]
        else:
            action_data = ""

        # Commands
        if action_type == "End":
            return
        elif action_type == "Wait":
            try:
                sleep_duration = parse_float(action_data)
                if globals.wait_with_delta:
                    sleep_duration += max(random.uniform(globals.random_waits[0], globals.random_waits[1]), 0)
            except ValueError:
                low, high = parse_float_tuple(action_data)
                sleep_duration = random.uniform(low, high)
            time.sleep(sleep_duration)
        elif action_type == "Trigger":
            x, y, target_color, wait_duration = parse_trigger_data(action_data)
            wait_start = datetime.now()

            screenshot = ImageGrab.grab(all_screens=True)
            pixel = screenshot.getpixel((x, y))
            while euclidean_distance(pixel, target_color) > globals.color_threshold:
                if panic:
                    panic_action()
                print_log("Pixel color: " + str(pixel))
                screenshot = ImageGrab.grab(all_screens=True)
                pixel = screenshot.getpixel((x, y))
                time.sleep(globals.refresh_rate)
                if wait_duration != -1 and (datetime.now() - wait_start).total_seconds() > wait_duration:
                    print_log("Trigger time exceeded, continue")
                    break
        elif action_type == "BranchTrigger":
            x, y, target_color, true_jump_point, false_jump_point = parse_branch_trigger_data(action_data)
            screenshot = ImageGrab.grab(all_screens=True)
            pixel = screenshot.getpixel((x, y))

            next_index = index + 1
            if euclidean_distance(pixel, target_color) < globals.color_threshold:
                if true_jump_point != "":
                    next_index = jump_points[true_jump_point]
                    print_log(f"Jumping to {true_jump_point}")

            else:
                if false_jump_point != "":
                    next_index = jump_points[false_jump_point]
                    print_log(f"Jumping to {false_jump_point}")
            index = next_index
            continue

        # Jump loop
        elif action_type == "Jump":
            if jump_counter[index][1] == -1:
                # Infinite jump
                next_index = jump_points[jump_counter[index][0]]
            else:
                # Find the next index to go to
                if jump_counter[index][1] > 0:
                    jump_counter[index][1] -= 1
                    print_log(f"Jumping to {jump_counter[index][0]}, remaining jump: {jump_counter[index][1]}")
                    next_index = jump_points[jump_counter[index][0]]
                else:
                    next_index = index + 1
                    jump_counter[index][1] = jump_counter[index][2]
            index = next_index
            continue

        # Mouse actions
        elif action_type == "Click":
            x, y = parse_mouse_pos_tuple(action_data)
            action.click_on_position(x, y)
        elif action_type == "RClick":
            x, y = parse_mouse_pos_tuple(action_data)
            action.click_on_position(x, y, "right")
        elif action_type == "MouseAction":
            x, y, button, button_state = parse_mouse_action(action_data)
            action.mouse_action(x, y, button, button_state == "down")
        elif action_type == "Drag":
            start_x, start_y, end_x, end_y, duration = parse_drag_data(action_data)
            action.mouse_drag(start_x, start_y, end_x, end_y, duration)
        elif action_type == "Scroll":
            x, y, scroll_amount = parse_scroll_data(action_data)
            action.mouse_scroll(x, y, int(scroll_amount))
        elif action_type == "MoveTo":
            x, y, duration = parse_move_to_data(action_data)
            action.move_to(x, y, duration)

        # Keyboard actions
        elif action_type == "Type":
            action.type_string(action_data)
        elif action_type == "Press":
            action.press_key(action_data)
        elif action_type == "KeyDown":
            action.hold_key(action_data, True)
        elif action_type == "KeyUp":
            action.hold_key(action_data, False)

        index += 1


def print_log(s):
    if globals.debug:
        print(s)


def panic_action():
    print("Panic received, exiting ...")
    exit(0)
