import setup
from setup import RPL
import post_to_web as PTW # see post_to_web.py for instructions
import time
import RoboPiLib as RPL

start = time.time()

x = 1

while True:
    x = 0
    RPL.servoWrite(1,0)
    RPL.servoWrite(2,0)
    x = x + 12
