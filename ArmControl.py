########################
    ## 0. INITIALIZE
########################
import RoboPiLib as RPL
import math

######### PINS ##########

### MOTOR 1 ###
motor1Control = 0
motor1ChannelA = 1
motor1EncoderPwrGnd = 2
motor1ChannelB =  3
###############

### MOTOR 2 ###
motor2Control = 4
motor2EncoderPwrGnd = 5
motor2ChannelA = 6
motor2ChannelB = 7
###############

#### PIN SETUP ####
RPL.pinMode(motor1Control, RPL.PWM)
RPL.pinMode(motor1ChannelA, RPL.INPUT)
RPL.pinMode(motor1ChannelB, RPL.INPUT)
RPL.pinMode(motor2Control, RPL.PWM)
RPL.pinMode(motor2ChannelA, RPL.INPUT)
RPL.pinMode(motor2ChannelB, RPL.INPUT)
###################
##########################

#### GLOBAL VARIABLES ####

#Initializes the count at starting position of arm - need to calculate starting position of angle 2
count1 = 0
count2 = 0

#Length of arms, from axle to axle
len1 = 12
len2 = 12

#for pwm motor control
freq = 3000

################################
    ## 1. USER INPUT
################################

#Takes x,y coordinate pair for the arm's endpoint requested destination
x = float(raw_input("x>"))
y = float(raw_input("y>"))

################################
    ## 2. INVERSE KINIMATICS
###############################
# inverse_kinimatic takes an x,y coordinate and returns it as two angles, a1 and a2


def LawOfCosines(a, b, c):
	C = math.acos((a*a + b*b - c*c) / (2 * a * b))
	return C

def distance(x, y):
	return math.sqrt(x*x + y*y)

def inverse_kinimatic(x, y):
	dist = distance(x, y)
	D1 = math.atan2(y, x)
	D2 = LawOfCosines(dist, len1, len2)
	A1 = D1 + D2
	B2 = LawOfCosines(len1, len2, dist)
	return A1, B1

def deg(rad):
	return rad * 180 / math.pi

################################
    ## 3. CONVERT ANGLES TO MECH. COUNT
################################
def angleToCount(angle):
    count = angle * 242.765
    return count

################################
    ## 4. RUN MOTOR
################################

# Runs motors until count = requested count
def runMotors(newCount1, newCount2):
    global count1
    global count2
    lastA1State = digitalRead(motor1ChannelA)
    lastA2State = digitalRead(motor2ChannelA)
    # Starts Motor1 and Motor2 in correct direction
    if newCount1 > count1:
        RPL.pwmWrite(motor1Control, 2000, freq)
    elif newCount1 < count1:
        RPL.pwmWrite(motor1Control, 1000, freq)
    else:
        RPL.pwmWrite(motor1Control, 1500, freq)
    if newCount2 > count2:
        RPL.pwmWrite(motor2Control, 2000, freq)
    elif newCount2 < count2:
        RPL.pwmWrite(motor2Control, 1000, freq)
    else:
        RPL.pwmWrite(motor2Control, 1500, freq)

    # Updates count from encoder1 and encoder2
    while count1 != newCount1 or count2 != newCount2:
        a1State = RPl.digitalRead(motor1ChannelA)
        if a1State != lastA1State: #reads channel a and b from encoder and updates the count
            if RPL.digitalRead(motor1ChannelB) != a1State:
                count1 += 1
            else:
                count1 -= 1
            lastA1State = a1State
            if count1 == newCount1: #if the current count equals the new count, stop the motor
                RPL.pwmWrite(motor1Control, 1500, freq)
        if a2State != lastA2State: #reads channel a and b from encoder and updates the count
            if RPL.digitalRead(motor2ChannelB) != a2State:
                count2 += 1
            else:
                count2 -= 1
            lastA2State = a2State
            if count2 == newCount2: #if the current count equals the new count, stop the motor
                RPL.pwmWrite(motor2Control, 1500, freq)




################################
    ## EXECUTE
################################
angle1, angle2 = angle(x,y)
newCount1 = angleToCount(angle1)
newCount2 = angleToCount(angle2)
runMotors(newCount1, newCount2)
