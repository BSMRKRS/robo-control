# ArmControlLib v0.2

###### Copyright Jack Rickman, 2018

Designed for Benilde St. Margaret's Rescue Robot, running on
Raspberry Pi 3's with RoboPi hats.

Utilizes the RoboPiLib library (RoboPyLib_pwmv0_97.py), from William Henning

## Setup:
Import ArmControlLib as ACL

From here on I will refer to ArmControlLib as ACL

ACL is an object based approach, designed to be used so that each physical motor
runs as its own object. Each type of motor has its own class. The current list
of supported motors is:

###### [1. Continous_Rotation_Servo](#1-continous_rotation_servo)
###### [2. Brushless_Encoded_Motor](#2-brushless_encoded_motor-1)
###### [3. Stepper_Motor](#3-stepper_motor-1)

ACL also contains an Inverse_Kinimatics class, currently only designed to work with
two Brushless_Encoded_Motor(s)
###### [4. Inverse_Kinimatics](#4-Inverse_Kinimatics)


## 1. Continous_Rotation_Servo
Establishment:
'servo1 = ACL.Continous_Rotation_Servo(controlPin, speed)''

Functions:
'servo1.clockwise()' turns motor on and runs it in a clockwise direction

'servo1.counterClockwise()' turns motor on and runs it in a counterClockwise direction

'servo1.stop()' stops the motor


## 2. Brushless_Encoded_Motor
Establishment: motor1 = ACL.Brushless_Encoded_Motor(controlPin, encoderPowerPin, Enc_A, Enc_B,
                 forward_speed, backward_speed, cycleEvents, freq)

  The first four variables are all pin numbers
  controlPin should be connected to a 5v supply on the RoboPiHat
  encoderPowerPin can be connected to any power pin

  Enc_A and Enc_B need to be connected to the RaspberryPi GPIO pins - NOT - the
  RoboPiHat. They will be GPIO numbers - google to find a diagram of GPIO pins on the
  RaspberryPi

  forward_speed and backward_speed are speed variables, for the pwm duty cycle between 0 and 3000
  with numbers further away from 1500 being either slower or faster

  cycleEvents is the number of countable events for the encoder in one full rotation
  Find this number by taking the manufacturer count and multiplying it by your gear rotation

  freq is the pwm frequency - 3000 works well with my current setup


Functions:
  motor1.clockwise() runs the motor in the clockwise direction

  motor1.counterClockwise runs the motor in a counterClockwise direction

  motor1.stop() stops the motor

  motor1.current_angle() returns the current angle of the motor, in degrees
  The current angle is based off the starting position of the motor, which is assumed to
  be zero degrees

  motor1.move_to_position(new_position) starts the motor in the either clockwise or counterClockwise
  direction based off the requested new_position. If the new_position is within an certain
  margin of error (default +- 5) of the current count, the motor will stop

## 3. Stepper_Motor
Establishment: motor1 = Stepper_Motor(dir_pin, pul_pin)

Functions:
motor1.clockwise() runs the stepper motor in the clockwise direction

motor1.counterClockwise() runs the stepper motor in the counterClockwise direction

motor1.move_steps(delta_step) moves the stepper motor a certain number of steps
if delta_step is positive, move delta_steps in clockwise direction
if delta_step is negative, move delta_step in counter-clockwise direction
