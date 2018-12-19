import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)
import go
import time

######################
## Motor Establishment
######################

motorL = 4
motorR = 3
motorR_forward = 2000
motorR_backward = 1000
motorL_forward = 1000
motorL_backward = 2000
c=0
front = 17
left = 17
right = 18

while c<13:
	c = c+1
	time.sleep(0.5)
	RPL.pinMode(front, RPL.INPUT)
	fr = RPL.digitalRead(front)
	print fr
	if fr == 1:
		print "stop"
		RPL.servoWrite(motorL, 1500)
		RPL.servoWrite(motorR, 1500)
	if fr == 0:
		print "go"
		go.go()
