import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

import time as time
import serial
import sys
import tty
import termios
import signal

######################
## Motor Establishment
######################

motorL = 3
motorR = 0

motorL_forward = 2000
motorL_backward = 1000
motorR_forward = 1750
motorR_backward = 1150
time1 = 1.215
time2 = 1.15

try:
  RPL.pinMode(motorL,RPL.SERVO)
  RPL.servoWrite(motorL,1500)
  RPL.pinMode(motorR,RPL.SERVO)
  RPL.servoWrite(motorR,1150)
except:
  pass

def stopAll():
  try:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)
  except:
    print "error except"
    pass



def forward():
   RPL.servoWrite(motorL,motorL_forward)

def reverse():
   RPL.servoWrite(motorL,motorL_backward)

def print_speed():
  print '--FORWARD: Left Motor: ', motorL_forward, ' Right Motor: ', motorR_forward, '\r'
  print '  BACKWARD: Left Motor: ', motorR_backward, ' Right Motor: ', motorL_backward, '\r'

def forwardSpeedChanges(change, mn = 1600, mx = 2900):
  global motorR_forward
  global motorL_forward
  motorR_forward += change
  motorL_forward += change
  motorR_forward = max(min(motorR_forward, mx), mn)
  motorL_forward = max(min(motorL_forward, mx), mn)
  print_speed()

def backwardSpeedChanges(change, mn = 100, mx = 1400):
  global motorR_backward
  global motorL_backward
  motorR_backward += change
  motorL_backward += change
  motorR_backward = max(min(motorR_backward, mx), mn)
  motorL_backward = max(min(motorL_backward, mx), mn)
  print_speed()

def backwardRightSpeedChange(change, mn = 1150, mx = 1750):
  global motorR_backward
  motorR_backward += change
  motorR_backward = max(min(motorR_backward, mx), mn)
  print_speed()

def backwardLeftSpeedChange(change, mn = 1000, mx = 1500):
  global motorL_backward
  motorL_backward += change
  motorL_backward = max(min(motorL_backward, mx), mn)
  print_speed()

def forwardRightSpeedChange(change, mn = 1150, mx = 1750):
  global motorR_forward
  motorR_forward += change
  motorR_forward = max(min(motorR_forward, mx), mn)
  print_speed()

def forwardLeftSpeedChange(change, mn = 1500, mx = 2000):
  global motorL_forward
  motorL_forward += change
  motorL_forward = max(min(motorL_forward, mx), mn)
  print_speed()


def on():
  RPL.servoWrite(motorR,motorR_forward)

def off():
  RPL.servoWrite(motorR,motorR_backward)

def pvc():
  RPL.servoWrite(motorR, 1250)

def wood():
  RPL.servoWrite(motorR, 1400)

fd = sys.stdin.fileno() # I don't know what this does
old_settings = termios.tcgetattr(fd) # this records the existing console settings that are later changed with the tty.setraw... line so that they can be replaced when the loop ends

######################################
## Other motor commands should go here
######################################

def interrupted(signum, frame): # this is the method called at the end of the alarm
  stopAll()

signal.signal(signal.SIGALRM, interrupted) # this calls the 'interrupted' method when the alarm goes off
tty.setraw(sys.stdin.fileno()) # this sets the style of the input

print "Ready To Drive! Press * to quit.\r"
## the SHORT_TIMEOUT needs to be greater than the press delay on your keyboard
## on your computer, set the delay to 250 ms with `xset r rate 250 20`
SHORT_TIMEOUT = 0.255 # number of seconds your want for timeout
while True:
  signal.setitimer(signal.ITIMER_REAL,SHORT_TIMEOUT) # this sets the alarm
  ch = sys.stdin.read(1) # this reads one character of input without requiring an enter keypress
  signal.setitimer(signal.ITIMER_REAL,0) # this turns off the alarm
  if ch == '*': # pressing the asterisk key kills the process
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) # this resets the console settings
    break # this ends the loop
  else:
    if ch == 'w':
      on()

    elif ch == 'a':
      forward()

    elif ch == 's':
      off()

    elif ch == 'd':
      reverse()

    elif ch == 'p':
      pvc()

    elif ch == 'o':
      wood()

    elif ch == "[":
      backwardSpeedChanges(-100)

    elif ch == "}":
      forwardSpeedChanges(-100)

    elif ch == "{":
      backwardSpeedChanges(100)

    elif ch == "6":
      forwardLeftSpeedChange(50)
      forward()

    elif ch == "5":
      forwardLeftSpeedChange(-50)
      forward()

    elif ch == "-":
      forwardRightSpeedChange(200)

    elif ch == "x":
      forwardRightSpeedChange(-100)

    elif ch == "3":
      backwardLeftSpeedChange(-50)
      reverse()

    elif ch == "4":
      backwardLeftSpeedChange(50)
      reverse()

    elif ch == "1":
      backwardRightSpeedChange(-50)
      off()

    elif ch == "2":
      backwardRightSpeedChange(50)
      off()

    else:
      stopAll()
