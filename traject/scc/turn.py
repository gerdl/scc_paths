"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""

import math

from property_manager import cached_property

import scipy.special
import numpy as np

from traject.scc import State


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

        return State(x, y, angles, kappa)

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

        return State(scale*ssa_csa[1], scale*ssa_csa[0], theta, kappa)

    def state_clothoid_second(self, s):
        """
        Parameters
        ----------
        s : np.array
        """
        assert ((s >= self.params.len_clothoid_part + self.len_of_circular_part).all())
        assert ((s <= 2*self.params.len_clothoid_part + self.len_of_circular_part).all())

        # inv_clothoid_s = 2 * self.params.len_clothoid_part + self.len_of_circular_part - s

        # calc the original clothoid, then rotate/translate
        # cloth_state = self.state_clothoid_first(inv_clothoid_s)
        # cloth_state = cloth_state.rotate_then_translate()

        scale = math.sqrt(math.pi / self.params.sigma_max)

        # run from len_clothoid_part to 0
        # NOTE: Mathematically, these brackets are nonsense, but in the numpy.array sense, they are absolutely necessary
        inv_clothoid_s = (2 * self.params.len_clothoid_part + self.len_of_circular_part) - s

        # TODO: I think something's still wrong here!
        ssa_csa = scipy.special.fresnel(inv_clothoid_s * math.sqrt(1 / (self.params.delta_min * math.pi)))

        # TODO: I think something's still wrong here!
        # theta changes quadratically with s
        theta = inv_clothoid_s * inv_clothoid_s / (2 * self.params.delta_min)

        # curvature changes linear until reaching kappa_max for s=len_clothoid_part
        kappa = inv_clothoid_s / self.params.len_clothoid_part * self.params.kappa_max

        state = State(-scale * ssa_csa[1], scale * ssa_csa[0], theta, kappa)

        state = state.rotate_then_translate(self.delta, self.state_qg.x,  self.state_qg.y)
        #state = state.rotate_then_translate(0, -self.params.state_qi.x, -self.params.state_qi.y)


        # return state.rotate_then_translate(self.delta, 0, 0)
        return state


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

    @cached_property
    def state_qj(self):
        """Where the inner circle segment intersects the second clothoid"""

        ang = self.delta - self.params.delta_min/2
        x = self.params.omega[0] + self.params.inner_rad * np.sin(ang)
        y = self.params.omega[1] - self.params.inner_rad * np.cos(ang)
        kappa = self.params.kappa_max

        return State(x, y, ang, kappa)

    @cached_property
    def state_qg(self):
        """The end of the second clothoid"""

        scale = self.params.outer_rad
        ang = self.delta
        # x = self.params.omega[0] + scale * (math.sin(self.delta - self.params.gamma) - math.sin(self.params.gamma))
        # y = self.params.omega[1] + scale * (math.cos(self.params.gamma) - math.cos(self.delta - self.params.gamma))

        #sin_term = math.sin(self.delta - self.params.gamma) - math.sin(self.params.gamma)
        #cos_term = math.cos(self.params.gamma) - math.cos(self.delta - self.params.gamma)

        #x = self.params.omega[0] * sin_term
        #y = self.params.omega[1] * cos_term

        st = State(-self.params.omega[0], -self.params.omega[1], 0, 0)
        st = st.rotate_then_translate(self.delta+2*self.params.gamma, self.params.omega[0], self.params.omega[1])

        return st
