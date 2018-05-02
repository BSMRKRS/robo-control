# robo-control
Terminal control for a RoboPi based robot
by lizzie mccracken :)

# Getting Started
1. Clone the repo with `git clone https://github.com/BSMRKRS/robo-control.git`
1. Enter the directory you made with `cd robo-control`
1. OPTIONAL: Change the keypress delay with `xset r rate 250 20`. This will remove the delay you see when you press a button to drive your robot.
1. Start the code with `python control.py`

# Driving
1. Use the WASD  keys to drive.
   * W : push linear actuator out
   * S : pull linear actuator in
   * A : rotate servo clockwise
   * D : rotate servo counterclockwise

1. Change the speed with the following keys:
   (I HAVE CHANGED IT SO IT IS NOT AFFECTING THE SPEED, BUT ACTING AS A STEPPER MOTOR FOR BOTH THE SERVO AND THE LINEAR ACTUATOR.)
   (WHEN YOU PRESS ONE OF THE FOLLOWING KEYS, IT WILL CHANGE THE "SPEED" OF THE MOTOR, AND ALSO RUN THE COMMAND AFTERWARDS)
   (THIS ALLOWS FOR THE LINEAR ACTUATOR AND SERVO TO MOVE IN SMALLER INCRIMENTS RATHER THAN ALL AT ONCE)

    * '1' and '2' will increase or decrese the amount the linear actuator extends
    * '3' and '4' will increase or decrease the revolutions the servo makes clockwise
    * '5' and '6' will increase or decrease the revolutions the servo makes counterclockwise

(disclaimer honestly not sure which goes clockwise or counterclockwise but they will work the same i'm just not sure which key is which)
(another disclaimer i have the linear actuator on pin 0 and the servo on pin 4, if you want to change it nano into the control.py file)

1. Press the asterisk (`*`) to quit controlling the robot.

# Changing the code
If you want to add control for more motors, you'll need to change the code in three places:
1. At the top define the motor pin number with `<<pin_name>> = <<pin_number>>, set the behavior of that pin with `RPL.pinMode(<<pin_name>>,RPL.SERVO)` Or whatever the mode is
1. In the `## Individual commands` section, define the function that will be called when you press a key.
1. In the loop that interprets the keypresses (i.e., below `while True`), you have to add another `elif ch == ` clause, and on the line below it, call the function you want to run when that key is pressed.


^^^ or in lizzie's terms:

1. you can create a command on the document, and then to set it to a specific key, scroll to the bottom and replace elif ch == '_' with the key you want to use, and put the command below it. 
1. this document defines the pin as motorL or motorR, and i have set the linear actuator as motorL and the servo as motorR.
