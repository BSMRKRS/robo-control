import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)
import xbox
import math

import sys, tty, termios, signal

######################
## Motor Establishment
######################

motorL = 0
motorR = 1


try:
  RPL.pinMode(motorL,RPL.SERVO)
  RPL.servoWrite(motorL, 1500)
  RPL.pinMode(motorR,RPL.SERVO)
  RPL.servoWrite(motorR, 1500)
except:
  pass


######################
## Individual commands
######################
def stopAll():
  try:
    RPL.servoWrite(motorL,1500)
    RPL.servoWrite(motorR,1500)
  except:
    print "error except"
    pass


def rightMotorScaled(x, y):
        a = y + x
        scaled = int(a * 750)
        return scaled + 1500

def leftMotorScaled(x, y):
        a = y - x
        scaled = int(a * 750)
        return scaled + 1500



if __name__ == '__main__':
    joy = xbox.Joystick()

    while not joy.Back():

        # Servo
        x, y = joy.leftStick()

        RPL.servoWrite(motorL,leftMotorScaled(x, y))
        RPL.servoWrite(motorR,rightMotorScaled(x, y))


joy.close()
stopAll()
