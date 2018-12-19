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
rreadings = []
lreadings = []
front = 16
left = 17
right = 18
#Left Turn Function
def turn9l(amnt):
        RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 2000)
        time.sleep(amnt)

#Right Turn Function
def turn9r(amnt):
        RPL.servoWrite(motorL, 1000)
        RPL.servoWrite(motorR, 1000)
        time.sleep(amnt)

#pause
def pause(amnt):
	RPL.servoWrite(motorL, 1500)
        RPL.servoWrite(motorR, 1500)
	time.sleep(amnt)

#Right n-Turn
def turn9nr(amnt):
	global rreadings, lreadings
	turn9l(amnt)
	pause(.2)
	RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 1000)
	time.sleep(3)
	pause(.2)
	turn9r(amnt*2)
	pause(.2)
	RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 1000)
	time.sleep(4)
	lreadings = []
	rreadings = []

#Right n-Turn
def turn9nl(amnt):
        global rreadings, lreadings
        turn9r(amnt)
        pause(.2)
        RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 1000)
        time.sleep(3)
        pause(.2)
        turn9l(amnt*2)
        pause(.2)
        RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 1000)
        time.sleep(4)
        lreadings = []
        rreadings = []
	

turn9nr(1.2)
	
RPL.servoWrite(motorL, 1500)
RPL.servoWrite(motorR, 1500)
