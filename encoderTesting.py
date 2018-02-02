
#import RPi.GPIO as GPIO
#import RoboPiLib_pwm as RPL
import threading
from time import sleep
from ArmControl import Motor
from ArmControl import Encoder
# RPL.RoboPiInit("/dev/ttyAMA0",115200)

LockRotary = threading.Lock()		# create lock for rotary switch?


# Main loop. Demonstrate reading, direction and speed of turning left/rignt
def main(encoder1):
    NewCounter = encoder1.Rotary_counter
    requestedCount = int(raw_input("> "))
    if NewCounter != requestedCount:
        # Starts Motor1 and Motor2 in correct direction
        if requestedCount > NewCounter:
            RPL.pwmWrite(0, 2500, 3000)
        elif requestedCount < NewCounter:
            RPL.pwmWrite(0, 500, 3000)
        else:
            RPL.pwmWrite(0, 1500, 3000)

    while True:								# start test
        sleep(0.01)								# sleep 100 msec
        print encoder1.Rotary_counter
        if abs(encoder1.Rotary_counter - requestedCount) < 5:
            RPL.pwmWrite(0, 1500, 3000)
            main(encoder1)


encoder1 = Encoder()
main(encoder1)
