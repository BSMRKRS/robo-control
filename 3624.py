import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

import time

######################
## Motor Establishment
######################

motorL = 0
motorR = 1
c = 0
motorR_forward = 2000
motorR_backward = 1000
motorL_forward = 1000
motorL_backward = 2000

front = 16
left = 17
right = 18
detect = False
count = False
wait = 0
backwards = False
ending = False
while c<300:
	c = c + 1
	time.sleep(0.1)
	sensor_pin = 0
	prox = RPL.analogRead(1)
	print prox
	if prox > 200:
		print "hey"
		detect = True
		if count == True:
			backwards = True
	else:
		print "lol"
		if detect == True:
			print "now"
			count = True
	if count == True:
		wait = wait + 0.1
		print "tick"
	if backwards == True:
		print "Here We Go"
		RPL.servoWrite(0,1000)
		RPL.servoWrite(1,2000)
		time.sleep(0.5+wait/2)
		RPL.servoWrite(0,1500)
                RPL.servoWrite(1,1500)
		time.sleep(1)
		RPL.servoWrite(0,1000)
                RPL.servoWrite(1,1000)
		time.sleep(1.2)
		RPL.servoWrite(0,2000)
                RPL.servoWrite(1,1000)
		time.sleep(5)
		break
	else:
		RPL.servoWrite(0,2000)
                RPL.servoWrite(1,1000)
RPL.servoWrite(motorL, 1500)
RPL.servoWrite(motorR, 1500)
