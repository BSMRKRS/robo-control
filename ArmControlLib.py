################################
# ArmControlLib v0.1
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
import threading
import time
import RPi.GPIO as GPIO
import RoboPiLib_pwm as RPL
import math
LockRotary = threading.Lock()

###############################
# Encoder Class
###############################


class Encoder(object):
    global LockRotary

    def __init__(self, Enc_A, Enc_B):
        self.Enc_A = Enc_A  # GPIO encoder pin A
        self.Enc_B = Enc_B  # GPIO encoder pin B
        self.Current_A = 1  # This assumes that Encoder inits while mtr is stopped
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

    def __init__(self, controlPin, encoderPowerPin, Enc_A, Enc_B,
                 forward_speed, backward_speed, cycleEvents, freq):
        self.controlPin = controlPin
        self.encoder = Encoder(Enc_A, Enc_B)
        self.forward_speed = forward_speed
        self.backward_speed = backward_speed
        self.cycleEvents = cycleEvents
        self.freq = freq
        self.encoderPowerPin = encoderPowerPin
        self.pinSetup()

    def pinSetup(self):
        RPL.pinMode(self.encoderPowerPin, RPL.OUTPUT)
        RPL.digitalWrite(self.encoderPowerPin, 1)
        RPL.pinMode(self.controlPin, RPL.PWM)

    def stop(self):
        RPL.pwmWrite(self.controlPin, 1500, self.freq)

    def forwards(self):
        RPL.pwmWrite(self.controlPin, 1500 + self.forward_speed, self.freq)

    def backwards(self):
        RPL.pwmWrite(self.controlPin, 1500 - self.backward_speed, self.freq)

    def current_angle(self):
        angle = self.encoder.Rotary_counter / self.cycleEvents
        angle = angle * 360
        return angle

    def move_to_position(self, new_position):
        if new_position <= self.encoder.Rotary_counter:
            self.forwards()
            print "Motor forwards"
        if new_position > self.encoder.Rotary_counter:
            self.backwards()
            print "Motor backwards"

############################
    # Inverse Kinimatics
############################


class Inverse_Kinimatics(object):

    def __init__(self, len1, len2, motor1, motor2):
        self.len1 = len1
        self.len2 = len2
        self.motor1 = motor1
        self.motor2 = motor2

    def LawOfCosines(self, a, b, c):
        C = math.acos((a * a + b * b - c * c) / (2 * a * b))
        return C

    def distance(self, x, y):
        return math.sqrt(x * x + y * y)

    def inverse_kinimatic(self, x, y):
        len1 = self.len1
        len2 = self.len2
        dist = self.distance(x, y)
        D1 = math.atan2(y, x)
        D2 = self.LawOfCosines(dist, len1, len2)
        A1 = D1 + D2
        B2 = self.LawOfCosines(len1, len2, dist)
        return A1, B1

    def deg(self, rad):
        return rad * 180 / math.pi

    def armKinimatics(self, x, y):
        angle1, angle2 = self.angle(x, y)
        newCount1 = self.angleToCount(angle1, self.motor1.cycleEvents)
        newCount2 = self.angleToCount(angle2, self.motor2.cycleEvents)
        self.runMotors(newCount1, newCount2)

    def angleToCount(self, angle, motorXCycleEvents):
        CycleEventsPerDegree = motorXCycleEvents / 360
        count = angle * CycleEventsPerDegree
        return count

    def runMotors(self, newCount1, newCount2):
        print "Motor1 newCount: %d" % newCount1
        print "Motor2 newCount: %d" % newCount2
        self.motor1.move_to_position(newCount1)  # Starts Motor1
        self.motor2.move_to_position(newCount2)  # Starts Motor2
        a = True
        b = True
        while a or b:
            sleep(0.001)
            print "Motor1 rot count: %d Motor2 rot count: %d" % (
                self.motor1.encoder.Rotary_counter, self.motor2.encoder.Rotary_counter)
            if abs(newCount1 - self.motor1.encoder.Rotary_counter) < 5:
                self.motor1.stop()
                a = False
                print "Motor 1 complete"

            if abs(newCount2 - self.motor2.encoder.Rotary_counter) < 5:
                self.motor2.stop()
                b = False
                print "Motor 2 complete"

    def angle(self, x, y):
        len1 = self.len1
        len2 = self.len2
        dist = self.distance(x, y)

        D1 = math.atan2(y, x)

        D2 = self.LawOfCosines(dist, len1, len2)

        A1 = D1 + D2

        A2 = self.LawOfCosines(len1, len2, dist)
        print self.deg(A1), self.deg(A2)

        return self.deg(A1), self.deg(A2)
