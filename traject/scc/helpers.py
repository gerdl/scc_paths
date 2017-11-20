"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""
import math


def calc_ang(dx, dy):
    ang = math.atan(dy / dx)
    # TODO: Take care of other quadrants
    return ang
