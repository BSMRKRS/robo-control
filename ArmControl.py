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


def ui():
    x = float(raw_input("x>"))
    y = float(raw_input("y>"))
    inverse_kinimatic_instance.armKinimatics(x, y)
    ui()

################################
# EXECUTE
################################


# Motor(controlPin, encoderPowerPin, Enc_A, Enc_B,
#          forward_speed, backward_speed, cycleEvents)


## Motor 1 ##
motor1 = ACL.Motor(2, 3, 19, 16, 1000, 1000, 21848.88, freq)


## Motor2 ##
motor2 = ACL.Motor(0, 1, 26, 20, 1000, 1000, 11098.56, freq)
inverse_kinimatic_instance = ACL.Inverse_Kinimatics(len1, len2, motor1, motor2)

ui()
