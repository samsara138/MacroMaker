# Features

Welcome to Macro Maker! Macro Maker is a versatile multitool designed to streamline the creation and execution of computer macros. 
This tool allows you to record and play both mouse and keyboard actions with ease.

The program can run in 3 modes:
1. **Play mode**: The default mode, read and play a macro file
2. **Record mode**: Capture your mouse and keyboard input and write them to a file
3. **Detector mode**: Log the mouse position and the pixel color of the pixel you are pointing at, if a key is pressed, log that too

# Run this program

### Requirement
Install requirement packages
```bash
  pip3 install -r requirment.txt
```

### Usage example
Execute a macro file 3 times
```bash
  py main.py -f maro_file.csv -i 3
```

Record a macro and save it to a file
```bash
  py main.py -r -f recorded_file.csv
```

Run in detector mode
```bash
  py main.py -d
```

**Note**: If you are playing an macro and want to stop the program but the macro player is taking control, use the ExecutionPanicKey (default: right alt) to stop the macro executor

## Creating a macro file
Macros are represented in csv files. In which, there are 2 required columns, ActionType and ActionData
The macro will be executed from the top row to the bottom row or until a End action is hit
Each row can represent a mouse or keyboard action, a comment/white space, or special commands. All can be found in the following table table

### Macro Maker Action Types and Data

| ActionType Format | ActionData Format                                      | Description                                                                                                                                                                                                                                                     | Example Data                                                 |
|-------------------|--------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| **Mouse**         |                                                        |                                                                                                                                                                                                                                                                 |                                                              |
| Click             | (x,y)                                                  | Simulates a left mouse click at (x,y).                                                                                                                                                                                                                          | (300,400)                                                    |
| RClick            | (x,y)                                                  | Simulates a right mouse click at (x,y).                                                                                                                                                                                                                         | (300,400)                                                    |
| Drag              | (x1,y1) &#124; (x2,y2) &#124; Duration"                | Simulates a mouse drag action from (x1,y1) to (x2,y2) over the specified duration.                                                                                                                                                                              | (100,100) &#124; (200,200) &#124; 1.5                        |
| MouseAction       | (x,y) &#124; (Button,Action)                           | Mostly used by recorder. Simulates a complex mouse action, at (x,y). Where the Button sepecify the button of action (left, right or middle) and Action the action to perform (up or down).                                                                      | (300,400) &#124; (left,down)                                 |
| Scroll            | (x, y) &#124; ScrollAmount                             | Simulates mouse scroll at position with the specified scroll amount.                                                                                                                                                                                            | (100, 200)                                                   | 5                                                  |
| MoveTo            | (x, y) &#124; Duration                                 | Use Duration amount of seconds to move mouse to position                                                                                                                                                                                                        | (100, 200)                                                   | 2                                                            |
| **Keyboard**      |                                                        |                                                                                                                                                                                                                                                                 |                                                              |
| Press             | Key                                                    | Simulates a key press (press down then release) for the specified key.                                                                                                                                                                                          | a                                                            |
| Type              | String                                                 | Simulate keyboard to types the specified string.                                                                                                                                                                                                                | Hello, World!                                                |
| KeyDown           | Key                                                    | Simulates a key being pressed down event for the specified key.                                                                                                                                                                                                 | space                                                        |
| KeyUp             | Key                                                    | Simulates a key being released event for the specified key.                                                                                                                                                                                                     | enter                                                        |
| **Logical**       |                                                        |                                                                                                                                                                                                                                                                 |                                                              |
| Wait              | WaitDuration or (MinDur, MaxDur)                       | Pauses execution for a exact amount of durations, or randomly select from a duration from a range                                                                                                                                                               | 5.2 or (2.0, 4.0)                                            |
| Trigger           | (x,y) &#124; (r,g,b) &#124; Wait (optional)            | Waits for a specific color at the specified position to continue execution. Optionally, you can specify a max amount of time to wait before going forward with the execution                                                                                    | (100,200) &#124; (255,0,0) &#124; 5.0                        |
| JumpPoint         | JumpPointName                                          | A point of execution that can be jump/return to                                                                                                                                                                                                                 | JumpPoint1                                                   |
| BranchTrigger     | (x,y) &#124; (r,g,b) &#124; TrueJump &#124; FalseJump" | Branches the macro based on a color trigger. If the color is found, it jumps to TrueJump point; otherwise, it jumps to FalseJump point. If any jump point is left blank, then when the condition is reached, the execution will simply move to the next command | (100,200) &#124; (255,0,0) &#124; TrueJump &#124; FalseJump" |
| Jump              | (Jump point identifier, LoopTime)                      | Jumps to the specified jump point in the macro, for at most LoopTime times                                                                                                                                                                                      | (JumpPoint1, 2)                                              |
| End               | N/A                                                    | Marks the end of the macro execution.                                                                                                                                                                                                                           | N/A                                                          |
| # Comment         | N/A                                                    | Add comment to your csv file for readability.                                                                                                                                                                                                                   | # This is a comment                                          |
| File              | FileName                                               | Replace this line with the data from another csv file                                                                                                                                                                                                           | file_name.csv                                                |
| Value             | (VariableName, VariableValue)                          | Set a int or float variable                                                                                                                                                                                                                                     | (TestVariable, 12)                                           |

## Recording mode
When in recorder mode, the recorder will wait for 3 seconds for you the get ready and start recording your mouse in keyboard input. 
It will track your mouse position when it's being pushed down or released, and track keyboard pressed. This tool is used mostly to assist the manual creation of a macro file. 
To make the resulting file more readable, use the RecorderBreakpointKey key (default: right ctrl) to insert a special in the csv file to indicate a transtion point of your macro file. 
Finally, press the RecorderExitKey (default: right alt) to end the recording and save it to a file
(The timing of the recorder is currently bugged, WIP)

## Edit the config file
The config.json allow you to customize some behaviour of the macro player

| Setting Name          | Usage                                                                                          | Default    |
|-----------------------|------------------------------------------------------------------------------------------------|------------|
| RefreshRate           | How often to read screen information (for triggers)                                            | 60         |
| ColorThreshold        | Allowed difference to register two colors as equal (for triggers and branching)                | 50         |
| ClickDuration         | During a click, the duration between pushing the mouse button down and releasing it            | 0.0005     |
| ScrollMultiplier      | Multiplier for scroll action                                                                   | 100        |
| WaitWithDelta         | Give all timed wait a delta to give it some variant between RandomWaitsLow and RandomWaitsHigh | false      |
| RandomWaitsLow        | When WaitWithDelta is true, minimal value of the delta                                         | -0.5       |
| RandomWaitsHigh       | When WaitWithDelta is true, maximum value of the delta                                         | 0.5        |
| RecorderExitKey       | Press this key to stop recording                                                               | right alt  |
| RecorderBreakpointKey | Press this key to add a breakpoint in the recording                                            | right ctrl |
| ExecutionPanicKey     | Press this key to stop the macro player                                                        | right alt  |
| XOffset               | Screen calibration X offset                                                                    | 1920       |
| YOffset               | Screen calibration Y offset                                                                    | 0          |
| Debug                 | Print debug logs to the terminal                                                               | false      |




