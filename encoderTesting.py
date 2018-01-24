
import RPi.GPIO as GPIO
import RoboPiLib_pwm as RPL
import threading
from time import sleep
RPL.RoboPiInit("/dev/ttyAMA0",115200)




LockRotary = threading.Lock()		# create lock for rotary switch?
OldCounter = 0
RPL.pinMode(0, RPL.PWM)
RPL.pinMode(1, RPL.OUTPUT)
RPL.digitalWrite(1, 1)

class Encoder(object):
	global LockRotary
	def __init__(self):
		self.Enc_A = 6							#GPIO encoder pin A
		self.Enc_B = 12							#GPIO encoder pin B
		self.Current_A = 1						#This assumes that Encoder is initaiate while the motor is not moving
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
		GPIO.add_event_detect(self.Enc_A, GPIO.RISING, callback=self.rotary_interrupt) 				# NO bouncetime
		GPIO.add_event_detect(self.Enc_B, GPIO.RISING, callback=self.rotary_interrupt) 				# NO bouncetime
		return

	def rotary_interrupt(self, A_or_B):
														# read both of the switches
		Switch_A = GPIO.input(self.Enc_A)
		Switch_B = GPIO.input(self.Enc_B)
														# now check if state of A or B has changed
														# if not that means that bouncing caused it
		if self.Current_A == Switch_A and self.Current_B == Switch_B:		# Same interrupt as before (Bouncing)?
			return										# ignore interrupt!

		self.Current_A = Switch_A								# remember new state
		Current_B = Switch_B								# for next bouncing check
		self.Current_B = Switch_B

		if (Switch_A and Switch_B):						# Both one active? Yes -> end of sequence
			LockRotary.acquire()						# get lock
			if A_or_B == self.Enc_B:							# Turning direction depends on
				self.Rotary_counter += 1						# which input gave last interrupt
			else:										# so depending on direction either
				self.Rotary_counter -= 1						# increase or decrease counter
			LockRotary.release()						# and release lock
		return											# THAT'S IT



# Main loop. Demonstrate reading, direction and speed of turning left/rignt
def main(encoder1):
	NewCounter = encoder1.Rotary_counter
	requestedCount = int(raw_input("> "))
	if NewCounter != requestedCount:
	    # Starts Motor1 and Motor2 in correct direction
	    if requestedCount > NewCounter:
	        RPL.pwmWrite(0, 2000, 3000)
	    elif requestedCount < NewCounter:
	        RPL.pwmWrite(0, 1000, 3000)
	    else:
	        RPL.pwmWrite(0, 1500, 3000)

	while True :								# start test
		sleep(0.01)								# sleep 100 msec
		print encoder1.Rotary_counter
		if abs(encoder1.Rotary_counter - requestedCount) < 10:
			RPL.pwmWrite(0, 1500, 3000)
			main(encoder1)
encoder1 = Encoder()
main(encoder1)
