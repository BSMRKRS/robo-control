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
fTime = True
front = 16
left = 17
right = 18
ideal = 300
tick  = 0
def turn9l(amnt):
	RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 2000)
	time.sleep(amnt)
	RPL.servoWrite(motorL, 1500)
        RPL.servoWrite(motorR, 1500)
def turn9r(amnt):
        RPL.servoWrite(motorL, 1000)
        RPL.servoWrite(motorR, 1000)
        time.sleep(amnt)
        RPL.servoWrite(motorL, 1500)
        RPL.servoWrite(motorR, 1500)

turn9r(1.1)
