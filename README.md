# robo-control
Terminal control for a RoboPi based robot

# Getting Started
1. Clone the repo with `git clone https://github.com/BSMRKRS/robo-control.git`
1. Enter the directory you made with `cd robo-control`
1. OPTIONAL: Change the keypress delay with `xset r rate 250 20`. This will remove the delay you see when you press a button to drive your robot.
1. Start the code with `python control.py`

# Driving
1. Use the WASD (and QEZC) keys to drive.
1. Change the speed with the following keys:
    * `[` and `]` change the forward speed of both motors.
    * `{` and `}` change the backward speed of both motors.
    * `1` and `!` increate and decrease the forward speed of the left motor
    * `2` and `@` increate and decrease the forward speed of the right motor
    * `3` and `#` increate and decrease the backward speed of the left motor
    * `4` and `$` increate and decrease the backward speed of the right motor
1. Press the asterisk (`*`) to quit controlling the robot.

# Changing the code
If you want to add control for more motors, you'll need to change the code in three places:
1. At the top define the motor pin number with `<<pin_name>> = <<pin_number>>, set the behavior of that pin with `RPL.pinMode(<<pin_name>>,RPL.SERVO)` Or whatever the mode is
1. In the `## Individual commands` section, define the function that will be called when you press a key.
1. In the loop that interprets the keypresses (i.e., below `while True`), you have to add another `elif ch == ` clause, and on the line below it, call the function you want to run when that key is pressed.
