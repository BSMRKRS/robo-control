import math
import sys
import pygame
import time
import socket

from ArmControlLib import Inverse_Kinimatics

socketRate = .1  # Make larger number to slow do info sent to Robot; larger number creates more latency; Too low of number sents too much info


arm = Inverse_Kinimatics(12.0, 12.0, 0, 0, 0, 0)


pygame.init()

size = width, height = 480, 480

black = 0, 0, 0,

x = 24.0
y = 0.0
screen = pygame.display.set_mode(size)

######################
# 5. Connect to Network
######################
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
server_address = (sys.argv[1], 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)


rectangle = [0, 240], [0, 190], [240, 190], [240, 240]
f = open('ftpTemp.txt', 'r+')


def ui():
    global x, y
    print "(%f, %f)" % (x, y)
    choice = raw_input(">")
    if choice == "coords":
        x = float(raw_input("x>"))
        y = float(raw_input("y>"))
        arm.armKinimatics(x, y)
    elif choice == "d":
        x += 1
        arm.armKinimatics(x, y)
    elif choice == "a":
        x -= 1
        arm.armKinimatics(x, y)
    elif choice == "w":
        y += 1
        arm.armKinimatics(x, y)
    elif choice == "s":
        y -= 1
        arm.armKinimatics(x, y)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    ui()
    sock.sendall(str(int(arm.data[0])) + ' ' + int(arm.data[1])))
    sleep(socketRate)

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
