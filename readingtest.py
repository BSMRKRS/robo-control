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
def turn9l():
        RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 2000)
        time.sleep(0.025)

#Right Turn Function
def turn9r():
        RPL.servoWrite(motorL, 1000)
        RPL.servoWrite(motorR, 1000)
        time.sleep(0.025)

def standardize(reading):
        reading = reading + 5
        reading = 2914 / reading
        reading = reading - 1
        return reading
######################
#  LOOP
######################

while c<10:
        c = c + .1
        time.sleep(slp)
        sensor_pin = 0
        lspd = RPL.analogRead(2)
        rspd = RPL.analogRead(1)
        fspd = RPL.analogRead(0)
        rspd = standardize(rspd)
        lspd = standardize(lspd)
        fspd = standardize(fspd)
        print rspd, lspd, fspd
        RPL.servoWrite(motorL,2000)
        RPL.servoWrite(motorR,1000)
