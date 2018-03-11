import math
import sys
import pygame
import time
from ArmControlLib import Inverse_Kinimatics


arm = Inverse_Kinimatics(12.0, 12.0, 0, 0)


pygame.init()

size = width, height = 480, 480

black = 0, 0, 0,

x = 24.0
y = 0.0
screen = pygame.display.set_mode(size)


rectangle = [0, 240], [0, 190], [240, 190], [240, 240]
f = open('ftpTemp.txt', 'r+')


def updateFTP():
    f.seek(0)
    for data in arm.data:
        f.write(str(data))
        f.write(" ")
    f.truncate()


def ui():
    global x, y
    print "(%f, %f)" % (x, y)
    choice = raw_input(">")
    if choice == "coords":
        x = float(raw_input("x>"))
        y = float(raw_input("y>"))
        arm.armKinimatics(x, y)
        updateFTP()
    elif choice == "d":
        x += 1
        arm.armKinimatics(x, y)
        updateFTP()
    elif choice == "a":
        x -= 1
        arm.armKinimatics(x, y)
        updateFTP()
    elif choice == "w":
        y += 1
        arm.armKinimatics(x, y)
        updateFTP()
    elif choice == "s":
        y -= 1
        arm.armKinimatics(x, y)
        updateFTP()


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ui()
    endpoints = [240, 190], [arm.shoulder_x, arm.shoulder_y], [
        arm.forarm_x, arm.forarm_y]
    endpoints_test = [240, 190], [arm.shoulder_x, arm.shoulder_y], [
        arm.forarm_x_test, arm.forarm_y_test]
    screen.fill([0, 0, 0])
    pygame.draw.circle(screen, [0, 200, 0], [240, 190], 240, 1)
    pygame.draw.polygon(screen, [200, 0, 0], rectangle, 5)
    pygame.draw.lines(screen, [0, 0, 200], False, endpoints_test, 5)
    pygame.draw.lines(screen, [200, 0, 0], False, endpoints, 5)
    pygame.display.flip()
