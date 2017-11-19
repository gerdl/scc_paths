"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""
import math


class State(object):
    def __init__(self, _x, _y, _theta, _kappa):
        self.x = _x
        self.y = _y
        self.theta = _theta
        self.kappa = _kappa

    def rotate_then_translate(self, alpha, dx, dy):
        ca = math.cos(alpha)
        sa = math.sin(alpha)
        x = self.x * ca - self.y * sa + dx
        y = self.x * sa + self.y * ca + dy
        th = self.theta + alpha
        return State(x, y, th, self.kappa)

    # so far, nobody uses this:
    #def reverse(self):
    #    theta = (self.theta + math.pi) % (math.pi*2)
    #    kappa = - self.kappa
    #    return State(self.x, self.y, theta, kappa)
