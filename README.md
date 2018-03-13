################################
# ArmControlLib v0.2
#
# Copyright Jack Rickman, 2018
#
# Designed to control Brushed DC motors with encoders
#
# Designed for Benilde St. Margaret's Rescue Robot, running on
# Raspberry Pi 3's with RoboPi hats.
#
# Utilizes the RoboPiLib library (RoboPyLib_pwmv0_97.py), from William Henning
#
##################################

How to use the Arm Control library (ArmControlLib.py)


Setup:
Import ArmControlLib as ACL

#From here on I will refer to ArmControlLib as ACL

ACL is an object based approach, designed to be used so that each physical motor
runs as its own object. Each type of motor has its own class. The current list
of supported motors is:
1. Continous_Rotation_Servo
2. Brushless_Encoded_Motor
3. Stepper_Motor

ACL also contains an Inverse_Kinimatics class, currently only designed to work with
two Brushless_Encoded_Motor(s)
4. Inverse_Kinimatics


1. Continous_Rotation_Servo
  Establishment: servo1 = ACL.Continous_Rotation_Servo(controlPin, speed)

  Functions:
  servo1.clockwise() turns motor on and runs it in a clockwise direction

  servo1.counterClockwise() turns motor on and runs it in a counterClockwise direction

  servo1.stop() stops the motor


2. Brushless_Encoded_Motor
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

  
