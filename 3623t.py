import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)
import math
import time

######################
#  VARIABLES
######################

#Motors
motorL = 0
motorR = 1

#Sensors
front = 16
left = 17
right = 18

#Clocks
rtick  = 0
ltick = 0
c = 0

#Which wall?
rwall = False
lwall = False

#Sleep amount
slp = 0.1

######################
#  LISTS
######################

#All readings
rreadings = []
lreadings = []

#Close wall readings
rwreadings = []
lwreadinggs = []

######################
#  FUNCTIONS
######################

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
#Straightening
def straight(rlist,dist):
	global rwall, lwall
        if len(rlist) > 6:
                if len(rlist) % 2 != 0:
                        rtrend = rlist[-5]-dist
                        if rtrend in range(-2,3):
                                pass
                        elif rtrend in range(-10,-3):
				if rwall == True:
					turn9l(0.01)
				elif lwall == True:
	                                turn9r(0.01)
                        elif rtrend in range(3,11):
				if lwall == True:	
        	                        turn9l(0.01)
				elif rwall == True:
					turn9r(0.01)
                        elif rtrend < -10:
				if lwall == True:
                                	turn9r(0.02)
				elif rwall == True:
					turn9l(0.02)
                        elif rtrend > 10:
				if lwall == True:
                                	turn9l(0.02)
				elif rwall == True:
					turn9r(0.02)
######################
#  LOOP
######################

while c<10:
        c = c + .1
        time.sleep(0.1)
        sensor_pin = 0
        lspd = RPL.analogRead(2)
        rspd = RPL.analogRead(1)
        rspd = int(2*92*math.log10(rspd))
        lspd = int(2*92*math.log10(lspd))
        #Convert it roughly linear readings
        rreadings.append(rspd)
        lreadings.append(lspd)
        if rspd > lspd:
                rwall = True
                lwall = False
        if lspd > rspd:
                lwall = True
                rwall = False
        if rwall == True:
                straight(rreadings,rspd)
        if lwall == True:
                straight(lreadings,lspd)
        RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 1000)
RPL.servoWrite(motorL, 1500)
RPL.servoWrite(motorR, 1500)
