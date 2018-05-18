################################
# ArmControl.py v0.2
#
# Copyright Jack Rickman, 2018
#
# Designed for a robotic arm with two encoded DC motors, elbow and shoulder.
#
# Designed for Benilde St. Margaret's Rescue Robot, running on
# Raspberry Pi 3's with RoboPi hats.
#
# Utilizes the RoboPiLib library (RoboPyLib_v0_97.py), from William Henning
#
# !!!Untested Alpha Program!!!
##################################

########################
# 0. INITIALIZE
########################
import RoboPiLib_pwm as RPL
import math
import threading
from time import sleep
import ArmControlLib as ACL
RPL.RoboPiInit("/dev/ttyAMA0", 115200)


# Length of arms, from axle to axle
len1 = 12
len2 = 12

# for pwm motor control
freq = 3000

x = 0
y = 0


def coords():
    global x, y
    inverse_kinimatic_instance.armKinimatics(x, y)
    ui()


def ui():
    global x, y
    print "(%f, %f)" % (x, y)
    choice = raw_input("Input:")
    if choice == "coords":
        x = float(raw_input("x>"))
        y = float(raw_input("y>"))
        coords()
    elif choice == "d":
        x += 1
        coords()
    elif choice == "a":
        x -= 1
        coords()
    elif choice == "w":
        y += 1
        coords()
    elif choice == "s":
        y -= 1
        coords()
    elif choice == "z":
        motor1.clockwise()
    elif choice == "x":
        motor1.counterClockwise()
    elif choice == "c":
        motor2.clockwise()
    elif choice == "v":
        motor2.counterClockwise()
    elif choice == "b":
        motor3.counterClockwise()
        sleep(0.1)
        motor4.counterClockwise()
    elif choice == "n":
        motor3.clockwise()
        sleep(0.1)
        motor4.clockwise()
    elif choice == "m":
        motor3.counterClockwise()
        sleep(0.1)
        motor4.clockwise()
    elif choice == "l":
        motor3.clockwise()
        sleep(0.1)
        motor4.counterClockwise()
    else:
        motor1.stop()
        sleep(0.01)
        motor2.stop()
        sleep(0.01)
        motor3.stop()
        sleep(0.01)
        motor4.stop()
    ui()
################################
# EXECUTE
################################


# Motor(controlPin, encoderPowerPin, Enc_A GPIO Pin, Enc_B GPIO Pin,
#          forward_speed, backward_speed, EncoderCyclesPerRotation, PWM frequency)


## Motor 1 ##
motor1 = ACL.Brushless_Encoded_Motor(0, 1, 26, 20, 1000, 1000, 21848.88, freq)


## Motor2 ##
motor2 = ACL.Brushless_Encoded_Motor(
    2, 3, 19, 16, -1000, -1000, 11098.56, freq)

motor3 = ACL.Continous_Rotation_Servo(4, 500)
motor4 = ACL.Continous_Rotation_Servo(5, 500)
inverse_kinimatic_instance = ACL.Inverse_Kinimatics(
    len1, len2, motor1, motor2, motor3, motor4)


ui()
