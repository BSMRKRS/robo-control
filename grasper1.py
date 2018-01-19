
import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

import sys, tty, termios, signal
import time

 RPL.servoWrite(0,1500)
 RPL.servoWrite(1,1500)
# Wait for 500 milliseconds
time.sleep(.500)
RPl.servoWrite(0,2000)
RPL.servoWrite(1,2000)
# wait for 500 milliseconds
time.sleep(.500)
RPL.servoWrite(0,1000)
RPL.servoWrite(0,1000)
time.sleep(.500)
RPL.servoWrite(0,1500)
RPL.servoWrite(1,1500)
time.sleep(.500)
RPL.servoWrite(0,0)
RPL.servoWrite(0,0)

# Wait for 300 milliseconds
# .3 can also be used
time.sleep(.300)
