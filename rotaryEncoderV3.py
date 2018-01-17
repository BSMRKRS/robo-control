
import RPi.GPIO as GPIO
import RoboPiLib_pwm as RPL
import threading
from time import sleep
RPL.RoboPiInit("/dev/ttyAMA0",115200)

						# GPIO Ports
Enc_A = 6 				# Encoder input A: input GPIO 4
Enc_B = 12		        # Encoder input B: input GPIO 14

Rotary_counter = 0  			# Start counting from 0
Current_A = 1					# Assume that rotary switch is not
Current_B = 1					# moving while we init software

LockRotary = threading.Lock()		# create lock for rotary switch
OldCounter = 0

# initialize interrupt handlers
def init():
	GPIO.setwarnings(True)
	GPIO.setmode(GPIO.BCM)					# Use BCM mode
											# define the Encoder switch inputs
	GPIO.setup(Enc_A, GPIO.IN)
	GPIO.setup(Enc_B, GPIO.IN)
											# setup callback thread for the A and B encoder
											# use interrupts for all inputs
	GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotary_interrupt) 				# NO bouncetime
	GPIO.add_event_detect(Enc_B, GPIO.RISING, callback=rotary_interrupt) 				# NO bouncetime
	return



# Rotarty encoder interrupt:
# this one is called for both inputs from rotary switch (A and B)
def rotary_interrupt(A_or_B):
	global Rotary_counter, Current_A, Current_B, LockRotary
													# read both of the switches
	Switch_A = GPIO.input(Enc_A)
	Switch_B = GPIO.input(Enc_B)
													# now check if state of A or B has changed
													# if not that means that bouncing caused it
	if Current_A == Switch_A and Current_B == Switch_B:		# Same interrupt as before (Bouncing)?
		return										# ignore interrupt!

	Current_A = Switch_A								# remember new state
	Current_B = Switch_B								# for next bouncing check


	if (Switch_A and Switch_B):						# Both one active? Yes -> end of sequence
		LockRotary.acquire()						# get lock
		if A_or_B == Enc_B:							# Turning direction depends on
			Rotary_counter += 1						# which input gave last interrupt
		else:										# so depending on direction either
			Rotary_counter -= 1						# increase or decrease counter
		LockRotary.release()						# and release lock
	return											# THAT'S IT

# Main loop. Demonstrate reading, direction and speed of turning left/rignt
def main():
	global Rotary_counter, LockRotary, OldCounter
	NewCounter = 0
	requestedCount = int(raw_input("> "))
	init()
	if NewCounter != requestedCount:
	    # Starts Motor1 and Motor2 in correct direction
	    if requestedCount > NewCounter:
	        RPL.pwmWrite(0, 500, 3000)
	    elif requestedCount < NewCounter:
	        RPL.pwmWrite(0, 2500, 3000)
	    else:
	        RPL.pwmWrite(0, 1500, 3000)

									# Init interrupts, GPIO, ...

	while True :								# start test
		sleep(0.1)								# sleep 100 msec

												# because of threading make sure no thread
												# changes value until we get them
												# and reset them

		LockRotary.acquire()					# get lock for rotary switch
		NewCounter = Rotary_counter		# get counter value
		LockRotary.release()
		if NewCounter == requestedCount:
			RPL.pwmWrite(0, 1500, 3000)
		if NewCounter != OldCounter:					# and release lock
			print NewCounter
			OldCounter = NewCounter		# some test print



# start main demo function
main()
