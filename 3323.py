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

while True:
	time.sleep(0.5)
	RPL.pinMode(left, RPL.INPUT)
	lft = RPL.digitalRead(left)
	RPL.pinMode(right, RPL.INPUT)
	rght = RPL.digitalRead(right)
	reading =  lft + rght
	print reading
	if reading  == 0:
		RPL.servoWrite(motorL, 2000)
		RPL.servoWrite(motorR, 1000)
	else:
		RPL.servoWrite(motorL, 1500)
		RPL.servoWrite(motorR, 1500)
RPL.servoWrite(motorL, 1500)
RPL.servoWrite(motorR, 1500)
