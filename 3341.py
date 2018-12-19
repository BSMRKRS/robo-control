import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

import time

######################
## Motor Establishment
######################

motorL = 0
motorR = 1

motorR_forward = 2000
motorR_backward = 1000
motorL_forward = 1000
motorL_backward = 2000

front = 16
left = 17
right = 18
c = 0
while c < 20:
	c = c+0.5
	time.sleep(0.5)
	RPL.pinMode(front, RPL.INPUT)
	fr = RPL.digitalRead(front)
	print fr
	if fr == 1:
		print "stop"
		RPL.servoWrite(motorL, 1500)
		RPL.servoWrite(motorR, 1500)
	if fr == 0:
		t = 0
		while t < 3:
			RPL.servoWrite(motorL, 1000)
                	RPL.servoWrite(motorR, 2000)
			time.sleep(1)
			c = c+1
                        RPL.servoWrite(motorL, 1500)
                        RPL.servoWrite(motorR, 1500)
                        time.sleep(1)
			c = c+1
			t = t+1
