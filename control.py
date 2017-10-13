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
motorL_forward = 2000
motorL_backward = 1000

try:
  RPL.pinMode(motorL,RPL.PWM)
  RPL.pwmWrite(motorL,1500,freq)
  RPL.pinMode(motorR,RPL.PWM)
  RPL.pwmWrite(motorR,1500,freq)
except:
  pass

######################
## Individual commands
######################
def stopAll():
  try:
    RPL.pwmWrite(motorL,1500, freq)
    RPL.pwmWrite(motorR,1500, freq)
  except:
    print "error except"
    pass

def forward():
  RPL.pwmWrite(motorL,motorL_forward, freq)
  RPL.pwmWrite(motorR,motorR_forward, freq)

def reverse():
  RPL.pwmWrite(motorL,motorL_backward, freq)
  RPL.pwmWrite(motorR,motorR_backward, freq)

def right():
  RPL.pwmWrite(motorL,motorL_forward, freq)
  RPL.pwmWrite(motorR,motorR_backward, freq)

def left():
  RPL.pwmWrite(motorL,motorL_backward,freq)
  RPL.pwmWrite(motorR,motorR_forward,freq)

def forward_right():
  RPL.pwmWrite(motorL,motorL_forward,freq)
  RPL.pwmWrite(motorR,1500,freq)

def forward_left():
  RPL.pwmWrite(motorL,1500,freq)
  RPL.pwmWrite(motorR,motorR_forward,freq)

def backward_right():
  RPL.pwmWrite(motorL,1500,freq)
  RPL.pwmWrite(motorR,motorR_backward,freq)

def backward_left():
  RPL.pwmWrite(motorL,motorL_backward,freq)
  RPL.pwmWrite(motorR,1500,freq)

def forwardSpeedChanges(change, mn = 1600, mx = 2900):
  global motorR_forward
  global motorL_forward
  motorR_forward += change
  motorL_forward += change
  motorR_forward = max(min(motorR_forward, mx), mn)
  motorL_forward = max(min(motorL_forward, mx), mn)
  print 'FORWARD: Left Motor: ', motorL_forward, ' Right Motor: ', motorR_forward, '\r'

def backwardSpeedChanges(change, mn = 100, mx = 1400):
  global motorR_backward
  global motorL_backward
  motorR_backward += change
  motorL_backward += change
  motorR_backward = max(min(motorR_backward, mx), mn)
  motorL_backward = max(min(motorL_backward, mx), mn)
  print 'BACKWARD: Left Motor: ', motorL_backward, ' Right Motor: ', motorR_backward, '\r'

def backwardRightSpeedChange(change, mn = 100, mx = 1400):
  global motorR_backward
  motorR_backward += change
  motorR_backward = max(min(motorR_backward, mx), mn)
  print 'BACKWARD: Left Motor: ', motorL_backward, ' Right Motor: ', motorR_backward, '\r'

def backwardLeftSpeedChange(change, mn = 100, mx = 1400):
  global motorL_backward
  motorL_backward += change
  motorL_backward = max(min(motorL_backward, mx), mn)
  print 'BACKWARD: Left Motor: ', motorL_backward, ' Right Motor: ', motorR_backward, '\r'

def forwardRightSpeedChange(change, mn = 1600, mx = 2900):
  global motorR_forward
  motorR_forward += change
  motorR_forward = max(min(motorR_forward, mx), mn)
  print 'FORWARD: Left Motor: ', motorL_forward, ' Right Motor: ', motorR_forward, '\r'

def forwardLeftSpeedChange(change, mn = 1600, mx = 2900):
  global motorL_forward
  motorL_forward += change
  motorL_forward = max(min(motorL_forward, mx), mn)
  print 'FORWARD: Left Motor: ', motorL_forward, ' Right Motor: ', motorR_forward, '\r'

SHORT_TIMEOUT = 0.2 # number of seconds your want for timeout

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
