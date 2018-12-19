import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)
import math
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

while c<15:
        c = c + .1
        time.sleep(0.1)
        sensor_pin = 0
        rspd = RPL.analogRead(2)
	lspd = RPL.analogRead(1)
	rspd = int(2*92*math.log10(rspd))
	lspd = int(2*92*math.log10(lspd))
	if rspd >500:
		rspd = 500
	if lspd > 500:
		lspd = 500
	if rspd > lspd:
		lspd = 0
	else:
		rspd = 0
	print rspd
	print lspd
	RPL.servoWrite(motorL, 2000-rspd)
	RPL.servoWrite(motorR, 1000+lspd)
RPL.servoWrite(motorL, 1500)
RPL.servoWrite(motorR, 1500)
