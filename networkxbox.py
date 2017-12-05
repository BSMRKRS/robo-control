import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)
import xbox
import math

import sys, tty, termios, signal

if __name__ == '__main__':
    joy = xbox.Joystick()

    while not joy.Back():
        x, y = joy.leftStick()
        print x
        print y
        xbox.refresh()
    joy.close()
