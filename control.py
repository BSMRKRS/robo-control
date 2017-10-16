import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

import sys, tty, termios, signal

######################
## Motor Establishment
######################

motorL = 0
motorR = 1

motorR_forward = 2000
motorR_backward = 1000
motorL_forward = 1000
motorL_backward = 2000

try:
  RPL.pinMode(motorL,RPL.SERVO)
  RPL.servoWrite(motorL,1500)
  RPL.pinMode(motorR,RPL.SERVO)
  RPL.servoWrite(motorR,1500)
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

def forward():
  RPL.servoWrite(motorL,motorL_forward)
  RPL.servoWrite(motorR,motorR_forward)
  print_speed()

def reverse():
  RPL.servoWrite(motorL,motorL_backward)
  RPL.servoWrite(motorR,motorR_backward)

def right():
  RPL.servoWrite(motorL,1460)#motorL_forward)
  RPL.servoWrite(motorR,1460)#motorR_backward)

def left():
  RPL.servoWrite(motorL,1540)#motorL_backward)
  RPL.servoWrite(motorR,1540)#motorR_forward)

def forward_right():
  RPL.servoWrite(motorL,motorL_forward)
  RPL.servoWrite(motorR,1500)

def forward_left():
  RPL.servoWrite(motorL,1500)
  RPL.servoWrite(motorR,motorR_forward)

def backward_right():
  RPL.servoWrite(motorL,1500)
  RPL.servoWrite(motorR,motorR_backward)

def backward_left():
  RPL.servoWrite(motorL,motorL_backward)
  RPL.servoWrite(motorR,1500)

def print_speed():
  print 'FORWARD: Left Motor: ', motorL_forward, ' Right Motor: ', motorR_forward, '\r'

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

def backwardRightSpeedChange(change, mn = 100, mx = 1400):
  global motorR_backward
  motorR_backward += change
  motorR_backward = max(min(motorR_backward, mx), mn)
  print_speed()

def backwardLeftSpeedChange(change, mn = 100, mx = 1400):
  global motorL_backward
  motorL_backward += change
  motorL_backward = max(min(motorL_backward, mx), mn)
  print_speed()

def forwardRightSpeedChange(change, mn = 1600, mx = 2900):
  global motorR_forward
  motorR_forward += change
  motorR_forward = max(min(motorR_forward, mx), mn)
  print_speed()

def forwardLeftSpeedChange(change, mn = 1600, mx = 2900):
  global motorL_forward
  motorL_forward += change
  motorL_forward = max(min(motorL_forward, mx), mn)
  print_speed()

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
      forward()
    elif ch == "a":
      left()
    elif ch == "s":
      reverse()
    elif ch == "d":
      right()
    elif ch == "e":
      forward_right()
    elif ch == "q":
      forward_left()
    elif ch == "z":
      backward_left()
    elif ch == "c":
      backward_right()
    elif ch == "]":
      forwardSpeedChanges(100)
    elif ch == "[":
      backwardSpeedChanges(-100)
    elif ch == "}":
      forwardSpeedChanges(-100)
    elif ch == "{":
      backwardSpeedChanges(100)
    elif ch == "1":
      forwardLeftSpeedChange(100)
    elif ch == "!":
      forwardLeftSpeedChange(-100)
    elif ch == "2":
      forwardRightSpeedChange(100)
    elif ch == "@":
      forwardRightSpeedChange(-100)
    elif ch == "3":
      backwardLeftSpeedChange(-100)
    elif ch == "#":
      backwardLeftSpeedChange(100)
    elif ch == "4":
      backwardRightSpeedChange(-100)
    elif ch == "$":
      backwardRightSpeedChange(100)
    else:
      stopAll()
