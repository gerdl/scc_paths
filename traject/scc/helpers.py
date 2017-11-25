"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""
import math


def calc_ang(dx, dy):

    if dx == 0:
        if dy >= 0:
            return math.pi/2
        else:
            return -math.pi/2

    ang = math.atan(dy / dx)

    if dx < 0:
        ang += math.pi
    # TODO: Take care of other quadrants
    return ang
