import RoboPiLib_pwm as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

##### Pins #####
controlPin = 0
channelAPin = 1
# VCCPin is attached to pwr for pin 2
#GNDPin is attached to gnd for pin 2
channelBPin = 3


#### Pin Setup ####
RPL.pinMode(controlPin, RPL.PWM)
RPL.pinMode(2, RPL.OUTPUT)
RPL.pinMode(channelAPin, RPL.INPUT)
RPL.pinMode(channelBPin, RPL.INPUT)
RPL.digitalWrite(2, 1)
#############
count1 = 0
a1State = 0
freq = 3000

def runMotors(newCount1):
    global count1
    lastA1State = RPL.digitalRead(channelAPin)
    # Starts Motor1 and Motor2 in correct direction
    if newCount1 > count1:
        RPL.pwmWrite(controlPin, 500, freq)
    elif newCount1 < count1:
        RPL.pwmWrite(controlPin, 2500, freq)
    else:
        RPL.pwmWrite(controlPin, 1500, freq)
    # Updates count from encoder
    while count1 != newCount1:
        a1State = RPL.digitalRead(channelAPin)
        if a1State != lastA1State: #reads channel a and b from encoder and updates the count (countable events)
            if RPL.digitalRead(channelBPin) != a1State:
                count1 += 1
            else:
                count1 -= 1
            lastA1State = a1State
    RPL.pwmWrite(controlPin, 1500, freq)
    print count1

runMotors(float(raw_input("> ")))
