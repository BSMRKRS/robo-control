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

#Gap measurer (Is the gap wide enough?)
gap = 0 

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
        time.sleep(2.5)
        pause(.2)
        turn9r(amnt*1.9)
        pause(.2)
        RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 1000)
        time.sleep(4)
        lreadings = []
        rreadings = []

#Left n-Turn
def turn9nl(amnt):
        global rreadings, lreadings
        turn9r(amnt)
        pause(.2)
        RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 1000)
        time.sleep(2.5)
        pause(.2)
        turn9l(amnt*1.9)
        pause(.2)
        RPL.servoWrite(motorL, 2000)
        RPL.servoWrite(motorR, 1000)
        time.sleep(5)
        lreadings = []
        rreadings = []

#Gap finder
def gap():
	global lwall, rwall, rreadings, lreadings
	s = 0
	frreadings = []
	flreadings = []
	resolved = False
	while s < 6:
		s = s+.1
		flspd = RPL.analogRead(2)
        	frspd = RPL.analogRead(1)
        	frspd = int(2*92*math.log10(frspd))
        	flspd = int(2*92*math.log10(flspd))
		print s, frspd, flspd
		frreadings.append(frspd)
		flreadings.append(flspd)
		if len(frreadings) > 9:
			if rwall == True:
				latest = int(rreadings[-3])
                                latest = latest-50
                                if frspd > latest:
					print "backtrack"
					RPL.servoWrite(motorR, 2000)
        				RPL.servoWrite(motorL, 1000)
					time.sleep(s/1.9)
					turn9nr(1.2)
					resolved = True
					break
				else:
					pass
			elif lwall == True:
				latest = int(lreadings[-3])
				latest = latest-10
                        	if flspd > latest:
					print "backtrack"
					RPL.servoWrite(motorR, 2000)
                                	RPL.servoWrite(motorL, 1000)
                                	time.sleep(s/1.9)
                                	turn9nl(1.2)
					resolved = True
					break
                        	else:
                                	pass 
		RPL.servoWrite(motorL, 2000)
        	RPL.servoWrite(motorR, 1000)
		time.sleep(.1)
	if resolved == True:
		pass
	else:
		RPL.servoWrite(motorR, 2000)
                RPL.servoWrite(motorL, 1000)
                time.sleep(s/2)
		if rwall == True:
			turn9nr(1.2)
		if lwall == True:
			turn9nl(1.2)
	

#Straightening
def straight(rlist,dist):
	global rwall, lwall, rreadings, lreadings
        if len(rlist) > 6:
                if len(rlist) % 2 != 0:
                        rtrend = rlist[-5]-dist
			#Compares the trend
			if dist-50 > rlist[-2]:
				gap() 
			else:
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
                        	elif rtrend in range(-11,-20):
					if lwall == True:
                                		turn9r(0.02)
					elif rwall == True:
						turn9l(0.02)
                        	elif rtrend > (11,20):
					if lwall == True:
                                		turn9l(0.02)
					elif rwall == True:
						turn9r(0.02)	
######################
#  LOOP
######################

while c<10:
	print len(rreadings)
	print len(lreadings)
        c = c + .1
        time.sleep(0.1)
        sensor_pin = 0
        lspd = RPL.analogRead(2)
        rspd = RPL.analogRead(1)
        rspd = int(2*92*math.log10(rspd))
        lspd = int(2*92*math.log10(lspd))
	print c, rspd, lspd
        #Convert it roughly linear readings
        rreadings.append(rspd)
        lreadings.append(lspd)
	if len(rreadings) > 5:
        	if rreadings[-5] > lreadings[-5]:
                	rwall = True
                	lwall = False
        	if lreadings[-5] > rreadings[-5]:
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
