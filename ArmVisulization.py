import math
import sys
import pygame
from ArmControlLib import Inverse_Kinimatics


arm = Inverse_Kinimatics(12.0, 12.0, 0, 0, 0, 0)


pygame.init()

size = width, height = 480, 480

black = 0, 0, 0,

x = 24.0
y = 0.0
screen = pygame.display.set_mode(size)


rectangle = [0, 240], [0, 190], [240, 190], [240, 240]
bound = 16.8
definition = 100
step = 2 * bound / definition
xMap = []
yMap = []


def ui():
    global x, y, xMap, yMap
    print "(%f, %f)" % (x, y)
    choice = raw_input(">")
    if choice == "coords":
        x = float(raw_input("x>"))
        y = float(raw_input("y>"))
        arm.visualization(x, y)
    elif choice == "d":
        x += 1
        arm.visualization(x, y)
        drawMap(xMap)
    elif choice == "a":
        x -= 1
        arm.visualization(x, y)
        drawMap(xMap)
    elif choice == "w":
        y += 1
        arm.visualization(x, y)
        drawMap(yMap)
    elif choice == "s":
        y -= 1
        arm.visualization(x, y)
        drawMap(yMap)
    xspeed, yspeed = arm.calcSpeed(x, y)
    print "y speed: %f" % yspeed
    print "x speed: %f" % xspeed
    cross(xspeed, yspeed)


def speedMapX():
    global xMap, bound, definition, step
    colorMapX = []
    for i in range(definition):
        for j in range(definition):
            try:
                dX = arm.calcSpeed(-bound + step * i, bound - step * j)[1]
                colorMapX.append(dX)
            except:
                colorMapX.append(0)
    xMap = colorMapX


def speedMapY():
    global yMap, xMap, bound, definition, step
    colorMapY = []
    for i in range(definition):
        for j in range(definition):
            try:
                dY = arm.calcSpeed(-bound + step * i, bound - step * j)[0]
                colorMapY.append(dY)
            except:
                colorMapY.append(0)
    yMap = colorMapY


def drawMap(speedmap):
    top = max(abs(min(speedmap)), max(speedmap))
    for i in range(len(speedmap)):
        perc = speedmap[i] / top
        shade = abs(int(255 * perc)), abs(int(255 * perc)
                                          ), abs(int(255 * perc))
        left = 240 - 168 + step * i * 10 - 5 * \
            step - math.floor(i / definition) * bound * 20
        upper = 190 - 168 + math.floor(i / definition) * step * 10 - 5 * step
        width = step * 10
        height = step * 10
        rect = pygame.Rect(left, upper, width, height)
        pygame.draw.rect(screen, shade, rect, 0)


def cross(xspeed, yspeed):
    xLine = [arm.forarm_x + xspeed * 5,
             arm.forarm_y], [arm.forarm_x - xspeed * 5, arm.forarm_y]
    yLine = [arm.forarm_x, arm.forarm_y + yspeed *
             5], [arm.forarm_x, arm.forarm_y - yspeed * 5]
    pygame.draw.line(screen, [0, 200, 0], [arm.forarm_x + xspeed * 5,
                                           arm.forarm_y], [arm.forarm_x - xspeed * 5, arm.forarm_y], 3)
    pygame.draw.line(screen, [0, 200, 0], [
                     arm.forarm_x, arm.forarm_y + yspeed * 5], [arm.forarm_x, arm.forarm_y - yspeed * 5], 3)


speedMapX()
speedMapY()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill([0, 0, 0])
    ui()
    endpoints = [240, 190], [arm.shoulder_x, arm.shoulder_y], [
        arm.forarm_x, arm.forarm_y]
    endpoints_test = [240, 190], [arm.shoulder_x, arm.shoulder_y], [
        arm.forarm_x_test, arm.forarm_y_test]
    pygame.draw.circle(screen, [0, 200, 0], [240, 190], 240, 1)
    pygame.draw.polygon(screen, [200, 0, 0], rectangle, 5)
    pygame.draw.lines(screen, [0, 0, 200], False, endpoints_test, 5)
    pygame.draw.lines(screen, [200, 0, 0], False, endpoints, 5)
    pygame.display.flip()
