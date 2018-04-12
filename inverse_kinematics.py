import math
import sys
import pygame
import time


class Arm(object):

    def __init__(self, len1, len2):
        self.len1 = 12.0
        self.len2 = 12.0
        self.a1 = float(0)
        self.a2 = float(0)
        self.shoulder_x = 150
        self.shoulder_y = 150
        self.forarm_x = 320
        self.forarm_y = 230
        self.data = [0, 0, 0, 0]
        self.moving = False
        #self.visualization(24, 0)
        # Speed stuff
        self.rot1 = 11
        self.rot2 = 23
        self.c1 = len1 * len2  # l1 * l2
        self.c2 = len1 + len2  # l1 + l2
        a = self.c2 / 2
        self.c3 = self.c1 - a  # c1 - 0.5c2
        b = 4 * len1
        self.c5 = 1 / b  # 1 / 4len1
        d = -1 * len1
        d = d + len2 ** 2
        self.c4 = d * self.c5  # (-len1 + len2^2)/c5
        e = len1 ** 4
        e = e + len2 ** 4
        e = e - 2 * self.c1
        e = e + 1
        self.c6 = e * self.c5  # (len1^4 + len2^4 - (2c1) + 1) * c5
        f = len1 ** 2
        f = f - len2
        g = 2 * len1
        c7 = f / g
        self.c8 = c7 + 1  # (len1^2 - len2) / (2len1)

    def shoulderEnd(self):
        self.shoulder_x = 240 + self.len1 * math.cos(self.a1) * 10
        self.shoulder_y = 190 - self.len1 * math.sin(self.a1) * 10

    def forarmEnd(self):
        self.forarm_x = self.shoulder_x + self.len2 * \
            math.cos(self.a2) * 10
        self.forarm_y = self.shoulder_y + self.len2 * \
            math.sin(self.a2) * 10

    def LawOfCosines(self, a, b, c):
        C = math.acos((a * a + b * b - c * c) / (2 * a * b))
        print "Law of Cosines: %f" % C
        return C

    def distance(self, x, y):
        print "distance: %f" % float(math.sqrt(x * x + y * y))
        return float(math.sqrt(x * x + y * y))

    def angles(self, x, y):
        dist = self.distance(x, y)
        self.calcSpeed(x, y, dist)

        D1 = math.atan2(y, x)
        print "D1: %d" % D1

        D2 = self.LawOfCosines(self.len1, dist, self.len2)
        print "D2: %d" % D2

        A1 = float(D1 + D2)

        A2 = float(self.LawOfCosines(self.len1, self.len2, dist))

        self.a1 = A1
        self.a2 = A2 + math.pi
        print "A1: %f A2: %f" % (self.a1, self.a2)
        self.shoulderEnd()
        self.forarmEnd()

    def deg(self, rad):
        return float(rad * 180 / math.pi)

    def v1(self, x, y, l3):
        a = 1 / l3
        a = a * self.c4 + l3 * self.c5
        b = math.sqrt(-1 * self.c6 * l3 ** 2 + self.c8)
        return a / b

    def v2(self, x, y, v1):
        return y ** 2 - x ** 2 + 2 * x * y * v1

    def speedY(self, x, y, l3, v1):
        v2 = self.v2(x, y, v1)
        a = self.c3 - 0.5 * l3 ** 3
        b = y + x * v1
        c = a + b
        c = c / v2
        c = c * self.rot1
        d = x * l3 ** 2
        d = d / v2
        e = self.rot2 * d
        return c - e

    def speedX(self, x, y, l3, speedY, v1):
        a = l3 ** 2
        a = a - x * speedY
        a = a - v1 * y * speedY
        b = v1 * x
        b = b + y
        c = a / b
        return self.rot1 * c

    def calcSpeed(self, x, y, l3):
        time_stamp = time.time()
        v1 = self.v1(x, y, l3)
        loc = speedY(x, y, l3, v1)
        # return loc, speedX(x, y, l3, loc, v1)
        print "dy/dt = %f" % loc
        print "dx/dt = %f" % speedX(x, y, l3, loc, v1)
        print "Time: "
        print time.time() - time_stamp


arm = Arm(12.0, 12.0)
x = float(raw_input("x>"))
y = float(raw_input("y>"))
arm.angles(x, y)
"""
pygame.init()

size = width, height = 480, 480

black = 0, 0, 0,


screen = pygame.display.set_mode(size)


rectangle = [0, 240], [0, 190], [240, 190], [240, 240]
arm = Arm()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    x = float(raw_input("x>"))
    y = float(raw_input("y>"))
    arm.angles(x, y)
    endpoints = [240, 190], [arm.shoulder_x, arm.shoulder_y], [
        arm.forarm_x, arm.forarm_y]
    screen.fill([0, 0, 0])
    pygame.draw.circle(screen, [0, 200, 0], [240, 190], 240, 1)
    pygame.draw.polygon(screen, [200, 0, 0], rectangle, 5)
    pygame.draw.lines(screen, [200, 0, 0], False, endpoints, 5)
    pygame.display.flip()
"""
