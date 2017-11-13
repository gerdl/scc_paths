"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""

import math

from property_manager import cached_property

import scipy.special
import numpy as np


class Turn(object):
    """This generates a turn that is always starting from angle 0, turning to an angle _delta"""

    def __init__(self, _params, _delta, _dir):
        """
        Parameters
        ----------
            _params : TurnParams
            _delta : float
                Deflection of th Turn
            _dir : int
                1 for left turn, -1 for right turn
        """

        self.params = _params
        self.delta = _delta
        self.dir = _dir

        assert(_delta > _params.delta_min)
        assert (_delta < 2 * math.pi)

    def state(self, s):
        """
        Returns
        -------
            tuple
                a 4-tuple of:
                - position x,
                - position y,
                - angle theta
                - curvature kappa

        Parameters
        ----------
            s : float
                the 1-d position along the turn path

        """
        pass

    def state_circular(self, s):
        # TODO: Fix the two-clothoids-only case:
        assert (self.delta > self.params.delta_min)

        assert ((s >= self.params.len_clothoid_part).all())
        assert ((s <= self.params.len_clothoid_part + self.len_of_circular_part).all())

        angular_segment = self.delta - self.params.delta_min
        start_angle = self.params.delta_min / 2.0
        angles = start_angle + (s - self.params.len_clothoid_part) / self.len_of_circular_part * angular_segment
        x = self.params.omega[0] + self.params.inner_rad * np.sin(angles)
        y = self.params.omega[1] - self.params.inner_rad * np.cos(angles)
        kappa = np.full([len(s)], self.params.kappa_max)

        return x, y, angles, kappa

    def state_clothoid_first(self, s):
        """
        Parameters
        ----------
        s : np.array
        """
        assert((s >= 0).all())
        assert((s <= self.params.len_clothoid_part).all())

        scale = math.sqrt(math.pi / self.params.sigma_max)

        # TODO: I think something's still wrong here!
        ssa_csa = scipy.special.fresnel(s * math.sqrt(1 / (self.params.delta_min * math.pi)))

        # TODO: I think something's still wrong here!
        # theta changes quadratically with s
        theta = s*s/(2*self.params.delta_min)

        # curvature changes linear until reaching kappa_max for s=len_clothoid_part
        kappa = s/self.params.len_clothoid_part * self.params.kappa_max

        return scale*ssa_csa[1], scale*ssa_csa[0], theta, kappa

    @cached_property
    def len_of_turn(self):
        pass

    @cached_property
    def len_of_circular_part(self):
        # circumference = 2*pi*r
        # angular_fraction = 2*pi / (delta - delta_min)

        angular_fraction = (self.delta - self.params.delta_min) / (2*math.pi)
        if angular_fraction < 0:
            return 0

        return 2 * math.pi * self.params.inner_rad * angular_fraction


