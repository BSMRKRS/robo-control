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


def LawOfCosines(a, b, c):
    C = math.acos((a * a + b * b - c * c) / (2 * a * b))
    return C


def distance(x, y):
    return math.sqrt(x * x + y * y)


def inverse_kinimatic(x, y):
    global len1, len2   # TODO: Fix hardwrite of length
    dist = distance(x, y)
    D1 = math.atan2(y, x)
    D2 = LawOfCosines(dist, len1, len2)
    A1 = D1 + D2
    B2 = LawOfCosines(len1, len2, dist)
    return A1, B1


def deg(rad):
    return rad * 180 / math.pi


def armKinimatics(x, y):
    angle1, angle2 = angle(x, y)
    newCount1 = angleToCount(deg(angle1), motor1.cycleEvents)
    newCount2 = angleToCount(deg(angle2), motor2.cycleEvents)
    runMotors(newCount1, newCount2)


def angleToCount(angle, motorXCycleEvents):
    CycleEventsPerDegree = motorXCycleEvents / 360
    count = angle * CycleEventsPerDegree
    return count


def runMotors(newCount1, newCount2):
    global motor1, motor2
    print "Motor1 newCount: %d" % newCount1
    print "Motor2 newCount: %d" % newCount2
    motor1.move_to_position(newCount1)  # Starts Motor1
    motor2.move_to_position(newCount2)  # Starts Motor2
    a = True
    b = True
    while a or b:
        sleep(0.001)
        if abs(newCount1 - motor1.encoder.Rotary_counter) < 5:
            motor1.stop()
            a = False
            print "Motor 1 complete"

        if abs(newCount2 - motor2.encoder.Rotary_counter) < 5:
            motor2.stop()
            b = False
            print "Motor 2 complete"


def angle(x, y):
    dist = distance(x, y)

    D1 = math.atan2(y, x)

    D2 = LawOfCosines(dist, len1, len2)

    A1 = D1 + D2

    A2 = LawOfCosines(len1, len2, dist)
    print A1, A2

    return A1, A2


def ui():
    x = float(raw_input("x>"))
    y = float(raw_input("y>"))
    armKinimatics(x, y)
    ui()

################################
# EXECUTE
################################


# Motor(controlPin, encoderPowerPin, Enc_A, Enc_B,
#          forward_speed, backward_speed, cycleEvents)


## Motor 1 ##
motor1 = ACL.Motor(0, 1, 19, 16, 1000, 1000, 21848.88, freq)


## Motor2 ##
motor2 = ACL.Motor(2, 3, 26, 20, 1000, 1000, 11098.56, freq)

ui()
