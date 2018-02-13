import math
import sys
import pygame


class Arm(object):

    def __init__(self):
        self.len1 = 12.0
        self.len2 = 12.0
        self.a1 = 0
        self.a2 = 0
        self.shoulder_x = 150
        self.shoulder_y = 150
        self.forarm_x = 320
        self.forarm_y = 230

    def shoulderEndpoint(self):
        self.shoulder_x = 240 + len1 * math.cos(self.a1) * 10
        self.shoulder_y = 190 - len1 * math.sin(self.a1) * 10

    def forarmEnd(self):
        self.forarm_x = self.shoulder_x + len2 * math.cos(self.a2) * 10
        self.forarm_y = self.shoulder_y + len2 * math.sin(self.a2) * 10


pygame.init()
armObj = Arm()
size = width, height = 320, 240
black = 255, 255, 255
shoulderEnd = [armObj.shoulder_x, armObj.shoulder_y]
forarmEnd = [armObj.forarm_x, armObj.forarm_y]
endpoints = [[0, 240], shoulderEnd, forarmEnd]
screen = pygame.display.set_mode(size)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    pygame.draw.lines(screen, [0, 0, 0], False, endpoints, 10)
    pygame.display.flip()
