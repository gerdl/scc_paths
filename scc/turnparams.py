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
from property_manager import cached_property
import scipy.special
import math

from scc import State


class TurnParams(object):
    """ rather abstract curve parameters that hold for any delta and direction """
    def __init__(self, _kappa_max, _sigma_max):
        self.kappa_max = _kappa_max      # the maximum curvature: inner radius: kappa_max^-1
        self.sigma_max = _sigma_max      # the steering rate; The sharpness of the turn

    @cached_property
    def inner_curve_radius(self):
        return 1.0 / self.kappa_max

    @cached_property
    def delta_min(self):
        return self.kappa_max * self.kappa_max / self.sigma_max

    @cached_property
    def len_clothoid_part(self):
        return self.kappa_max / self.sigma_max

    @cached_property
    def inner_rad(self):
        return 1.0 / self.kappa_max

    @cached_property
    def outer_rad(self):
        """The radius of the outer circle, encapsulating the turn"""
        return math.sqrt(self.omega[0] * self.omega[0] + self.omega[1] * self.omega[1])

    @cached_property
    def omega(self):
        """The position of the center of the outer/inner circle.  (left-turn)"""
        x_qi = self.state_qi.x
        y_qi = self.state_qi.y
        xo = x_qi - math.sin(self.state_qi.theta) / self.kappa_max
        yo = y_qi + math.cos(self.state_qi.theta) / self.kappa_max
        return xo, yo

    @cached_property
    def omega_r(self):
        """The position of the center of the outer/inner circle of a right-turn."""
        xo, yo = self.omega
        return xo, -yo

    @cached_property
    def state_qi(self):
        """Where the first clothoid intersects the inner circle (left-turn)"""
        scale = math.sqrt(math.pi / self.sigma_max)

        ssa_csa = scipy.special.fresnel(math.sqrt(self.delta_min/math.pi))
        theta = self.delta_min / 2
        kappa = self.kappa_max

        st = State(
            _x=scale*ssa_csa[1],
            _y=scale*ssa_csa[0],
            _theta=theta,
            _kappa=kappa
        )
        return st

    @cached_property
    def state_qi_r(self):
        """Where the first clothoid intersects the inner circle in a right-turn"""
        s = self.state_qi
        s.y *= -1
        return s

    @cached_property
    def gamma(self):
        """The angle between the outer circle tangent and the start/end vector."""
        gamma = math.atan(self.omega[0] / self.omega[1])
        return gamma
