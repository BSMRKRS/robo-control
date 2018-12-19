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
motorL_forward = 100\=]
motorL_backward = 2000

front = 16
left = 17
right = 18
detect = False
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
		detect == True
	else:
		if detect == True:
			if count > 0:
				backwards = True
		else:
			pass				
	if count == True:
		wait = wait + 0.1
	if backwards == True
		RPL.servoWrite(0,1000)
		RPL.servoWrite(1,2000)
		time.sleep(wait/2)
		RPL.servoWrite(0,1500)
                RPL.servoWrite(1,1500)
		time.sleep(1)
		RPL.servoWrite(0,1000)
                RPL.servoWrite(1,1000)
		time.sleep(2)
		RPL.servoWrite(0,1000)
                RPL.servoWrite(1,2000)
		time.sleep(2)
		ending = True
	else:
		RPL.servoWrite(0,2000)
                RPL.servoWrite(1,1000)
	if ending == True:
		break
RPL.servoWrite(motorL, 1500)
RPL.servoWrite(motorR, 1500)
