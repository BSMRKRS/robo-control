import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

import time

######################
## Motor Establishment
######################

motorL = 1
motorR = 0

motorR_forward = 2000
motorR_backward = 1000
motorL_forward = 1000
motorL_backward = 2000

c = 0
num = 0
while c < 0.5:
	c = c+0.5
	time.sleep(0.5)
	sensor_pin = 16
	RPL.pinMode(sensor_pin,RPL.INPUT)
	reading = RPL.digitalRead(sensor_pin)
	print reading
RPL.servoWrite(motorL, 1500)
RPL.servoWrite(motorR, 1500)
