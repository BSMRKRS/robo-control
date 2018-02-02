################################
#
# ArmControl.py v0.1
#
# Copyright Jack Rickman, 2018
#
# Designed for a robotic arm with two encoded DC motors, elbow and shoulder.
#
# (0.) Initializes RaspberryPi, RoboPiLib, and other libraries. Holds all
# variables based on hardware setup, pins, and other customizables.
#
# (1.) Takes a requested (x,y) coordinate in the arms range of motion
# 	!!!Comment (1.) out if using ArmControl.py for iterating through (x,y) coord
#
# (2.) Translates (x,y) into the necessary angles of the arm beams for the endp
# be at (x,y)

# (3.) From there the angles are translated into the countable events from enco
#
# (4.) The program then runs the motors until the counted events from the encod
# equal to the requested number of events , moving the motors to the correct
# angles, and moving the endpoint of the arm to the correct (x,y)
# posistion.
#
# Assumes the starting position for the endpoint is (0,0) -- if it is not, find
#
# Designed for Benilde St. Margaret's Rescue Robot, running on
# Raspberry Pi 3's with RoboPi hats.
#
# Utilizes the RoboPiLib library (RoboPyLib_v0_97.py), from William Henning
#
# !!!Untested Alpha Program!!!
#
########################
# 0. INITIALIZE
########################
import RoboPiLib_pwm as RPL
import math
import RPi.GPIO as GPIO
import threading
from time import sleep
RPL.RoboPiInit("/dev/ttyAMA0", 115200)

# PINS #


##########################

# GLOBAL VARIABLES #


# Length of arms, from axle to axle
len1 = 12
len2 = 12

# for pwm motor control
freq = 3000

# Countable events per revolution of output shaft !!! This includes the motors
# internal gear ratio, and
# the external gear ratio !!! Currently, the motor counts 5462.22 events pe
# output revolution, and
# is on a 16:1 ratio, so motor1CycleEvents = 5462.22 * 16 = 87395.52 events for
# one full revolution of the joint

# Ditto motor1^^^, can be different if two motors have different encoders


################################
# 1. USER INPUT
################################

# Takes x,y coordinate pair for the arm's endpoint requested destination
# If this program is to be used to increment through (x,y) coordinates along a
# plane/automatically,
# comment this section out, and increment through armKinimatics(x,y) using an
# outside program to increment through
# values.
x = float(raw_input("x>"))
y = float(raw_input("y>"))

################################
# 2. INVERSE KINIMATICS
###############################
# inverse_kinimatic takes an x,y coordinate and returns it as two angles


class Inverse_Kinimatics():
    global motor1, motor2

    def LawOfCosines(a, b, c):
        C = math.acos((a * a + b * b - c * c) / (2 * a * b))
        return C

    def distance(x, y):
        return math.sqrt(x * x + y * y)

    def inverse_kinimatic(x, y):
        dist = distance(x, y)
        D1 = math.atan2(y, x)
        D2 = LawOfCosines(dist, len1, len2)
        A1 = D1 + D2
        B2 = LawOfCosines(len1, len2, dist)
        return A1, B1

    def deg(rad):
        return rad * 180 / math.pi

    def armKinimatics(x, y):
        angle1, angle2 = Inverse_Kinimatics.angle(x, y)
        newCount1 = Inverse_Kinimatics.angleToCount(angle1, motor1.cycleEvents)
        newCount2 = Inverse_Kinimatics.angleToCount(angle2, motor2.cycleEvents)
        while a or b:

    def angleToCount(angle, motorXCycleEvents):
        CycleEventsPerDegree = motorXCycleEvents / 360
        count = angle * CycleEventsPerDegree
        return count


################################
    # 3. CONVERT ANGLES TO MECH. COUNT
################################


################################
    # 3. ENCODER
################################
class Encoder(object, Enc_A, Enc_B):
    global LockRotary

    def __init__(self):
        self.Enc_A = Enc_A  # GPIO encoder pin A
        self.Enc_B = Enc_B  # GPIO encoder pin B
        self.Current_A = 1  # This assumes that Encoder inits while mtr is stop
        self.Current_B = 1
        self.Rotary_counter = 0
        self.startEncoders()

    def startEncoders(self):
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)					# Use BCM mode?
        # define the Encoder switch inputs ?
        GPIO.setup(self.Enc_A, GPIO.IN)
        GPIO.setup(self.Enc_B, GPIO.IN)
        # setup callback thread for the A and B encoder
        # use interrupts for all inputs
        GPIO.add_event_detect(self.Enc_A, GPIO.RISING,
                              callback=self.rotary_interrupt) 	# NO bouncetime
        GPIO.add_event_detect(self.Enc_B, GPIO.RISING,
                              callback=self.rotary_interrupt) 	# NO bouncetime
        return

    def rotary_interrupt(self, A_or_B):
        # read both of the switches
        Switch_A = GPIO.input(self.Enc_A)
        Switch_B = GPIO.input(self.Enc_B)
        # now check if state of A or B has changed
        # if not that means that bouncing caused it
        # Same interrupt as before (Bouncing)?
        if self.Current_A == Switch_A and self.Current_B == Switch_B:
            return										# ignore interrupt!

        self.Current_A = Switch_A								# remember new state
        Current_B = Switch_B								# for next bouncing check
        self.Current_B = Switch_B

        if (Switch_A and Switch_B):		# Both one active? Yes -> end of sequence
            LockRotary.acquire()		# get lock
            if A_or_B == self.Enc_B:		# Turning direction depends on
                self.Rotary_counter += 1		# which input gave last interrupt
            else:								# so depending on direction either
                self.Rotary_counter -= 1		# increase or decrease counter
            LockRotary.release()				# and release lock
        return									# THAT'S IT

###############################
    # Motor Class
###############################


class Motor(object):
    global freq

    def __init__(self):
        self.motor_number = 0
        self.controlPin = 0
        self.encoderPowerPin = 0
        self.ChannelA = 0
        self.ChannelB = 0
        self.forward_speed = 1000
        self.backward_speed = 1000
        self.encoder = 0
        self.cycleEvents = 0

    def stop(self):
        RPL.pwmWrite(self.controlPin, 1500, freq)

    def forwards(self):
        RPL.pwmWrite(self.controlPin, 1500 + speed, freq)

    def backwards(self):
        RPL.pwmWrite(self.controlPin, 1500 - speed, freq)

    def current_angle(self):
        angle = self.encoder.Rotary_counter / self.cycleEvents
        angle = angle * 360
        return angle

    def move_to_position(self, new_position):
        if new_position > self.encoder.Rotary_counter:
            self.forwards()
        if new_position < self.encoder.Rotary_counter:
            self.backwards()
        else:
            self.stop()
        while abs(self.encoder.Rotary_counter - new_position) > 5:
            time.sleep(0.01)
        self.stop()

################################
    # EXECUTE
################################


encoder1 = Encoder(motor1ChannelA, motor1ChannelB)
motor1 = Motor()
motor1.controlPin = 0
motor1.encoderPowerPin = 1
motor1.encoder = encoder1
motor1.forward_speed = 1000
motor1.backward_speed = 1000
motor1.cycleEvents = 21848.88


encoder2 = Encoder(motor2ChannelA, motor2ChannelB)
motor2 = Motor()
motor2.controlPin = 2
motor2.encoderPowerPin = 3
motor2.encoder = encoder2
motor2.forward_speed = 1000
motor2.backward_speed = 1000
motor2.cycleEvents = 11098.56


Inverse_Kinimatics.armKinimatics(x, y)
