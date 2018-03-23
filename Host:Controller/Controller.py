
#######################
# 0. Initialization
########################
import pygame  # controller


# Initialize pygame
pygame.init()
pygame.display.init()
pygame.joystick.init()


#### GLOBAL VARIABLES ####

# left and right joystick dead zones (current dead zone for ps4 controller)
xDeadZoneLeft = 0.06
yDeadZoneLeft = 0.06
xDeadZoneRight = 0.06
yDeadZoneRight = 0.06

# motor speeds (assumes there is the same possible speeds going in reverse)
maxMotorL = 1000
maxMotorR = 1000

# Arm position
armX = 0
armY = 0

#########################
# 1. UI
#########################


# Weclome Screen
print "#" * 60
print "Welcome to the BSM robot controller support python program!"
print "#" * 60
print "I recommend choosing the joystick layout."
print "For support please visit https://github.com/avoss19/Robot-Controller-Support"
print "#" * 60
print "#" * 60

# Defualts to joystick control if input was not put in correctly
#########################
# 2. READ JOYSTICK
#########################

# get joystick readings


def joysticks():
    global xAxisLeft, yAxisLeft, xAxisRight, yAxisRight, triggerLeft, triggerRight

    pygame.event.get()

    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        xAxisLeft = joystick.get_axis(0)  # Why are these in the for loop?
        yAxisLeft = joystick.get_axis(1)

        xAxisRight = joystick.get_axis(2)
        yAxisRight = joystick.get_axis(3)

        triggerLeft = joystick.get_axis(4)
        triggerRight = joystick.get_axis(5)
###########################
# 3. INTERPRET JOYSTICK
# \

# Interpret Drive Motors


def driveMotors():
    motorSpeedL = 0
    motorSpeedR = 0
    motorL = 0
    motorR = 0
    if -yDeadZoneRight < yAxisRight < yDeadZoneRight:
        motorSpeedL = 0
        motorSpeedR = 0

    else:
        motorSpeedL = maxMotorL * -yAxisRight
        motorSpeedR = maxMotorR * -yAxisRight

    if -xDeadZoneRight < xAxisRight < xDeadZoneRight:
        motorL = motorSpeedL
        motorR = motorSpeedR

    elif xAxisRight <= 0:
        motorL = motorSpeedL - (motorSpeedL * (-xAxisRight))
        motorR = motorSpeedR

    elif xAxisRight > 0:
        motorL = motorSpeedL
        motorR = motorSpeedR + (motorSpeedR * (-xAxisRight))

    return motorL, motorR

# Interpret arm controls


def armJoystickInterpret():
    global armX, armY
    if time.time() - updateTime >= delay:
        if not -yDeadZoneLeft < yAxisLeft < yDeadZoneLeft:
            armX = armX + yAxisLeft  # Need to find a good scale
        if triggerRight == 1:
            armY += 0.1
        if triggerLeft == 1:
            armY -= 0.1


def KitBotSpeed(speed):
    center = 1500
    return speed + center


def updateFTP():
    data = [inverse_kinimatic_instance.data[0],
            inverse_kinimatic_instance.data[1], time.time()]
    f.seek(0)
    f.truncate()
    for i in data:
        f.write(str(data[i]))
        f.write(" ")


# -------------------Main Program--------------------------
f = open('ftpTemp', 'r+')
while True:
    updateFTP()
