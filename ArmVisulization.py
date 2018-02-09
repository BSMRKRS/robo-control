import math
import sys
import pygame
import ArmControlLib as ACL


class Arm(object):

    def __init__(self):
        self.len1 = 12.0
        self.len2 = 12.0
        self.a1 = 0
        self.a2 = 0

    def shoulderEndpoint(self):
        self.shoulder_x = 240 + len1 * math.cos(self.a1) * 10
        self.shoulder_y = 190 - len1 * math.sin(self.a1) * 10

    def forarmEnd(self):
        self.forarm_x =
        self.forarm_y =
