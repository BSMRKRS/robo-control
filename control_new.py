#This combines the speed changes so there is only a forward
# and backward speed change.

import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

import sys, tty, termios, signal

######################
## Motor Establishment
######################

motorL = 0
motorR = 1

motor_forward= 1760
motor_backward = 1160

try:
  RPL.pinMode(motorL,RPL.SERVO)
  RPL.servoWrite(motorL,1460)
  RPL.pinMode(motorR,RPL.SERVO)
  RPL.servoWrite(motorR,1460)
except:
  pass

######################
## Individual commands
######################
def stopAll():
  try:
    RPL.servoWrite(motorL,1460)
    RPL.servoWrite(motorR,1460)
  except:
    print "error except"
    pass

def forward():
  RPL.servoWrite(motorL,motor_forward)
  RPL.servoWrite(motorR,motor_forward)

def reverse():
  RPL.servoWrite(motorL,motor_backward)
  RPL.servoWrite(motorR,motor_backward)

def right():
  RPL.servoWrite(motorL,motor_forward)
  RPL.servoWrite(motorR,1460)

def left():
  RPL.servoWrite(motorL,1460)#motorL_backward)
  RPL.servoWrite(motorR,motor_forward)#motorR_forward)

def forward_right():
  RPL.servoWrite(motorL,motor_forward)
  RPL.servoWrite(motorR,1660)

def forward_left():
  RPL.servoWrite(motorL,1660)
  RPL.servoWrite(motorR,motor_forward)

def backward_right():
  RPL.servoWrite(motorL,1260)
  RPL.servoWrite(motorR,motor_backward)

def backward_left():
  RPL.servoWrite(motorL,motor_backward)
  RPL.servoWrite(motorR,1260)

def print_speed():
  print '--FORWARD: ', motor_forward, '\r'
  print '  BACKWARD:', motor_backward, '\r'

def forwardSpeedChanges(change, mn = 960, mx = 1960):
  global motorR_forward
  global motorL_forward
  motor_forward += change
  motor_forward = max(min(motor_forward, mx), mn)
  print_speed()

def backwardSpeedChanges(change, mn = 100, mx = 1400):
  global motorR_backward
  global motorL_backward
  motor_backward += change
  motor_backward = max(min(motor_backward, mx), mn)
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
    elif ch == "o":
      forwardSpeedChanges(100)
    elif ch == "l":
      backwardSpeedChanges(-100)
    elif ch == "p":
      forwardSpeedChanges(-100)
    elif ch == ";":
      backwardSpeedChanges(100)
    else:
      stopAll()
