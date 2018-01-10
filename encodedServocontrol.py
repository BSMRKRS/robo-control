import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

##### Pins #####
directionPin = 0
channelAPin = 1
# VCCPin is attached to pwr for pin 2
#GNDPin is attached to gnd for pin 2
channelBPin = 3
speedPin = 4

#### Pin Setup ####
RPL.pinMode(directionPin, RPL.Output)
RPL.pinMode(channelAPin, RPL.Input)
RPL.pinMode(channelBPin, RPL.Input)
RPL.pinMode(speedPin, RPL.Output)
#############
count = 0
aState = 0
lastAState = RPL.digitalRead

while True:
    aState = RPl.digitalRead(channelAPin)
    if aState != lastAState:
        if RPL.digitalRead(channelBPin) != aState:
            count += 1
        else:
            count -= 1
        lastAState = aState
        print count
