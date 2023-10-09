import json
import time
import argparse

from macro_maker import globals, macro_player
from macro_maker import macro_file_reader
from macro_maker.macro_recorder import recorder
from macro_maker.macro_recorder import AutoCursorInfoLogger
from macro_maker.screen_calibration import start_calibration

need_calibration = False


def parse_args():
    """
    Parse args to globals
    """
    parser = argparse.ArgumentParser(description='Macro maker')

    parser.add_argument('-f', '--file_name', type=str, default="test_data.csv",
                        help='Name of the macro file to execute or to write if in record mode (default test_data.csv)')

    parser.add_argument('-i', '--iterations', type=int, default=1,
                        help='How many time to run the macro')

    parser.add_argument('-r', '--record', action='store_true',
                        help='Count down for 3 seconds, then record mouse click and keyboard presses')

    parser.add_argument('-d', '--detector', action='store_true',
                        help='Run in detector mode')

    parser.add_argument('-c', '--calibration', action='store_true',
                        help='Run in calibration mode')

    args = parser.parse_args()
    globals.file_name = args.file_name
    globals.iterations = args.iterations
    globals.record_mode = args.record
    globals.detect_mode = args.detector
    globals.calibration_mode = args.calibration


def read_config():
    """
    read and parse config.json to globals
    """
    with open("config.json", "r") as json_file:
        data = json.load(json_file)

        globals.refresh_rate = 1 / data["Execution"]["RefreshRate"]
        globals.color_threshold = data["Execution"]["ColorThreshold"]
        globals.click_duration = data["Execution"]["ClickDuration"]
        globals.scroll_multiplier = data["Execution"]["ScrollMultiplier"]
        globals.wait_with_delta = data["Execution"]["WaitWithDelta"]
        globals.random_waits = (data["Execution"]["RandomWaitsLow"], data["Execution"]["RandomWaitsHigh"])

        globals.recorder_exit_key = data["Keybind"]["RecorderExitKey"]
        globals.recorder_breakpoint_key = data["Keybind"]["RecorderBreakpointKey"]
        globals.execution_panic_key = data["Keybind"]["ExecutionPanicKey"]

        if "Calibration" in data:
            globals.x_offset = data["Calibration"]["XOffset"]
            globals.y_offset = data["Calibration"]["YOffset"]
        else:
            # If the calibration data is never generated, require calibration
            global need_calibration
            need_calibration = True

        globals.debug = data["Debug"]


def play_mode():
    """
    Load and execute the macro file
    """
    macro_file = globals.file_name
    print(f"Loading {macro_file} ...")
    macro_data = macro_file_reader.read_data(macro_file)
    time.sleep(1)
    print("Executing")
    for i in range(globals.iterations):
        macro_player.execute_macro(macro_data)
    print("Success")


def record_mode():
    """
    Record and save macro to file
    """
    print("Start in 3 seconds, every mouse click (at position) and keyboard press will be recorded")
    time.sleep(3)
    data = recorder.start_recording()
    macro_file = globals.file_name
    print(f"writing to {macro_file} ...")
    macro_file_reader.write_date(data, macro_file)


def main():
    parse_args()
    read_config()

    global need_calibration
    if need_calibration:
        user_input = input("You haven't calibrated your screen yet, the marco may not execute correctly. Do you want to calibrate your screen? (y/n)").lower()
        if user_input == 'y':
            globals.calibration_mode = True

    if globals.calibration_mode:
        start_calibration()
    elif globals.record_mode:
        record_mode()
    elif globals.detect_mode:
        AutoCursorInfoLogger.log_cursor_position()
    else:
        play_mode()


if __name__ == '__main__':
    main()
