# --------------------------------File on Latop---------------------------------
# Reads controller input and connects to robot
import os
import sys
import socket
import pygame
from time import sleep

#### Global Variables ####

socketRate = .1  # Make larger number to slow do info sent to Robot; larger number creates more latency; Too low of number sents too much info

# left and right joystick dead zones (current dead zone for ps4 controller)
xDeadZoneLeft = 0.06
yDeadZoneLeft = 0.06
xDeadZoneRight = 0.06
yDeadZoneRight = 0.06

# motor speeds (assumes there is the same possible speeds going in reverse)
maxShoulder = 1250
maxElbow = 1250
shoulder = 0
elbow = 0

######################
# 0. Initialization
######################
pygame.init()
pygame.display.init()
pygame.joystick.init()

######################
# 2. Controller Reading
######################


def controllerInput():
    global xAxisLeft, yAxisLeft, xAxisRight, yAxisRight, triggerLeft, triggerRight
    global buttonSquare, buttonX, buttonCircle, buttonTriangle
    global dpadleft, dpadright, dpaddown, dpadup, bumperL, bumperR

    dpadleft = 0
    dpadright = 0
    dpaddown = 0
    dpadup = 0

    pygame.event.get()

    try:
        joystick = pygame.joystick.Joystick(0)
    except:
        print "ERROR: Controller not found!"
        print "#" * 60
        exit()

    joystick.init()

    xAxisLeft = joystick.get_axis(0)
    yAxisLeft = joystick.get_axis(1)

    xAxisRight = joystick.get_axis(2)
    yAxisRight = joystick.get_axis(3)

    triggerLeft = joystick.get_axis(4)
    triggerRight = joystick.get_axis(5)

    buttonSquare = joystick.get_button(0)
    buttonX = joystick.get_button(1)
    buttonCircle = joystick.get_button(2)
    buttonTriangle = joystick.get_button(3)

    bumperL = joystick.get_button(4)
    bumperR = joystick.get_button(5)

    # dpad works w/ PS4 controller, but not xbox
    # dpad = joystick.get_hat(0)
    # dpadxaxis = dpad[0]
    # dpadyaxis = dpad[1]

    # if dpadxaxis > 0:
    #    dpadright = dpadxaxis
    # if dpadxaxis < 0:
    #    dpadleft = -dpadxaxis
    # if dpadyaxis > 0:
    #    dpadup = dpadyaxis
    # if dpadyaxis < 0:
    #    dpaddown = -dpadyaxis


######################
# 3. Inturpret Joystick
######################
def armMotors():
    global shoulder, elbow

    if -yDeadZoneRight < yAxisRight < yDeadZoneRight:
        shoulder = 0
    else:
        shoulder = maxShoulder * -yAxisRight

    if -yDeadZoneLeft < yAxisLeft < yDeadZoneLeft:
        elbow = 0
    else:
        elbow = maxElbow * -yAxisLeft

    return shoulder, elbow


######################
# 4. Convert to KitBot
######################
def Speed(speed):
    center = 1500
    return speed + center


######################
# 5. Connect to Network
######################
try:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port on the server given by the caller
    server_address = (sys.argv[1], 10000)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
except:
    print "#" * 60
    print "ERROR: Failed to connect to host"
    print "#" * 60
    exit()


######################
##      Main        ##
######################

while True:
    controllerInput()
    data = armMotors()
    try:
        sock.sendall(
            str(str(int(Speed(data[0]))) + ' ' + str(int(Speed(data[1])))))
        sleep(socketRate)

    except:
        print "Error: Failed to connect to Robot"
        exit()

    os.system('clear')
