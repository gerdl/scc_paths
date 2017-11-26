"""
    Simple Continuous Curvature Path Library

    Copyright (C) 2017, Gerd Gruenert

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
        th = (self.theta + alpha) % (2*math.pi)
        return State(x, y, th, self.kappa)

    # so far, nobody uses this:
    #def reverse(self):
    #    theta = (self.theta + math.pi) % (math.pi*2)
    #    kappa = - self.kappa
    #    return State(self.x, self.y, theta, kappa)
