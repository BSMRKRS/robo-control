import math
import sys
import pygame

pygame.init()

size = width, height = 480, 480

black = 0, 0, 0,


screen = pygame.display.set_mode(size)


len1 = 12.0
len2 = 12.0


def LawOfCosines(a, b, c):
    C = math.acos((a * a + b * b - c * c) / (2 * a * b))
    return C


def distance(x, y):
    return math.sqrt(x * x + y * y)


def angles(x, y):
    dist = distance(x, y)

    D1 = math.atan2(y, x)

    D2 = LawOfCosines(dist, len1, len2)

    A1 = D1 + D2

    A2 = LawOfCosines(len1, len2, dist)

    return A1, A2


def shoulderEndpoint(a1):
    x = 240 + len1 * math.cos(a1) * 10
    y = 190 - len1 * math.sin(a1) * 10
    print x, y
    return x, y


def deg(rad):
    return rad * 180 / math.pi


rectangle = [0, 240], [0, 190], [240, 190], [240, 240]


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    x = float(raw_input("x>"))
    y = float(raw_input("y>"))
    a1, a2 = angles(x, y)
    shoulderEnd = shoulderEndpoint(a1)
    forarmEnd = 240 + 10 * x, 190 - 10 * y
    endpoints = [240, 190], shoulderEnd, forarmEnd
    screen.fill([0, 0, 0])
    pygame.draw.circle(screen, [0, 200, 0], [240, 190], 240, 1)
    pygame.draw.polygon(screen, [200, 0, 0], rectangle, 5)
    pygame.draw.lines(screen, [200, 0, 0], False, endpoints, 5)
    pygame.display.flip()
