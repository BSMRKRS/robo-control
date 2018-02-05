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
import RPi.GPIO as GPIO
import threading
from time import sleep
LockRotary = threading.Lock()
RPL.RoboPiInit("/dev/ttyAMA0", 115200)


# Length of arms, from axle to axle
len1 = 12
len2 = 12

# for pwm motor control
freq = 3000


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
        Inverse_Kinimatics.runMotors(newCount1, newCount2)

    def angleToCount(angle, motorXCycleEvents):
        CycleEventsPerDegree = motorXCycleEvents / 360
        count = angle * CycleEventsPerDegree
        return count

    def runMotors(newCount1, newCount2):
        global motor1, motor2, encoder1, encoder2, freq
        motor1.move_to_position(newCount1)  # Starts Motor1
        motor2.move_to_position(newCount2)  # Starts Motor2
        a = True
        b = True
        while a or b:

            if abs(newCount1 - encoder1.Rotary_counter) < 5:
                motor1.stop()
                a = False
                print "Motor 1 complete"

            if abs(newCount2 - encoder2.Rotary_counter) < 5:
                motor2.stop()
                b = False
                print "Motor 2 complete"


################################
    # 3. ENCODER
################################
class Encoder(object):
    global LockRotary

    def __init__(self, Enc_A, Enc_B):
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

        self.Current_A = Switch_A						# remember new state
        Current_B = Switch_B							# for next bouncing check
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

    def __init__(self, controlPin, encoderPowerPin, forward_speed,
                 backward_speed, encoder, cycleEvents):
        self.controlPin = controlPin
        self.forward_speed = forward_speed
        self.backward_speed = backward_speed
        self.encoder = encoder
        self.cycleEvents = cycleEvents
        self.pinSetup(encoderPowerPin)

    def pinSetup(self, encoderPowerPin):
        RPL.pinMode(encoderPowerPin, RPL.OUTPUT)
        RPL.digitalWrite(encoderPowerPin, 1)
        RPL.pinMode(self.controlPin, RPL.PWM)

    def stop(self):
        RPL.pwmWrite(self.controlPin, 1500, freq)

    def forwards(self):
        RPL.pwmWrite(self.controlPin, 1500 + forward_speed, freq)

    def backwards(self):
        RPL.pwmWrite(self.controlPin, 1500 - backward_speed, freq)

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

################################
    # EXECUTE
################################


# Takes x,y coordinate pair for the arm's endpoint requested destination
# If this program is to be used to increment through (x,y) coordinates along a
# plane/automatically,
# comment this section out, and increment through armKinimatics(x,y) using an
# outside program to increment through
# values.
x = float(raw_input("x>"))
y = float(raw_input("y>"))

# Motor(controlPin, encoderPowerPin, encoder, forward_speed, backward_speed, cycleEvents)

## Motor 1 ##
encoder1 = Encoder(19, 16)
motor1 = Motor(0, 1, encoder1, 1000, 1000, 21848.88))


## Motor2 ##
encoder2=Encoder(26, 20)
motor2=Motor(2, 3, encoder2, 1000, 1000, 11098.56))


Inverse_Kinimatics.armKinimatics(x, y)
