import math
import sys
import pygame


class Arm(object):

    def __init__(self):
        self.len1 = 12.0
        self.len2 = 12.0
        self.a1 = float(0)
        self.a2 = float(0)
        self.shoulder_x = 150
        self.shoulder_y = 150
        self.forarm_x = 320
        self.forarm_y = 230

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
