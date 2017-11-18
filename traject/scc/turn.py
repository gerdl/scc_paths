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

    def __init__(self, _params, _delta):
        """
        Parameters
        ----------
            _params : TurnParams
            _delta : float
                Deflection of th Turn; positive = left turn, negative = right turn
            _dir : int
                1 for left turn, -1 for right turn
        """

        self.params = _params
        self.delta = math.fabs(_delta)
        self.dir = 1
        if _delta < 0:
            self.dir = -1

        assert(self.delta > _params.delta_min)
        assert (self.delta < 2 * math.pi)

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

        first_clotho_cond = s < self.params.len_clothoid_part
        circ_seg_cond = (s > self.params.len_clothoid_part) & \
                        (s < self.params.len_clothoid_part + self.len_of_circular_part)
        second_clotho_cond = (s > self.params.len_clothoid_part + self.len_of_circular_part)

        x = np.empty(len(s))
        y = np.empty(len(s))
        theta = np.empty(len(s))
        kappa = np.empty(len(s))

        first_clotho = self._state_clothoid_first(s[first_clotho_cond])
        x[first_clotho_cond] = first_clotho.x
        y[first_clotho_cond] = first_clotho.y
        theta[first_clotho_cond] = first_clotho.theta
        kappa[first_clotho_cond] = first_clotho.kappa

        circ_seg = self._state_circular(s[circ_seg_cond])
        x[circ_seg_cond] = circ_seg.x
        y[circ_seg_cond] = circ_seg.y
        theta[circ_seg_cond] = circ_seg.theta
        kappa[circ_seg_cond] = circ_seg.kappa

        second_clotho = self._state_clothoid_second(s[second_clotho_cond])
        x[second_clotho_cond] = second_clotho.x
        y[second_clotho_cond] = second_clotho.y
        theta[second_clotho_cond] = second_clotho.theta
        kappa[second_clotho_cond] = second_clotho.kappa

        return State(x, self.dir * y, self.dir * theta, self.dir * kappa)

    def _state_circular(self, s):
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

    def _state_clothoid_first(self, s):
        """ left turn, first clothoid segment

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

    def _state_clothoid_second(self, s):
        """
        Parameters
        ----------
        s : np.array
        """
        assert ((s >= self.params.len_clothoid_part + self.len_of_circular_part).all())
        assert ((s <= 2*self.params.len_clothoid_part + self.len_of_circular_part).all())

        scale = math.sqrt(math.pi / self.params.sigma_max)

        # run from len_clothoid_part to 0
        # NOTE: Mathematically, these brackets are nonsense, but in the numpy.array sense, they are absolutely necessary
        inv_clothoid_s = (2 * self.params.len_clothoid_part + self.len_of_circular_part) - s

        ssa_csa = scipy.special.fresnel(inv_clothoid_s * math.sqrt(1 / (self.params.delta_min * math.pi)))

        # theta changes quadratically with s
        theta = - inv_clothoid_s * inv_clothoid_s / (2 * self.params.delta_min)

        # curvature changes linear until reaching kappa_max for s=len_clothoid_part
        kappa = inv_clothoid_s / self.params.len_clothoid_part * self.params.kappa_max

        state = State(-scale * ssa_csa[1], scale * ssa_csa[0], theta, kappa)
        state = state.rotate_then_translate(self.delta, self._state_qg.x,  self._state_qg.y)
        return state

    @cached_property
    def len(self):
        return self.len_of_circular_part + 2*self.params.len_clothoid_part

    @cached_property
    def len_of_circular_part(self):
        # circumference = 2*pi*r
        # angular_fraction = 2*pi / (delta - delta_min)

        angular_fraction = (self.delta - self.params.delta_min) / (2*math.pi)
        if angular_fraction < 0:
            return 0

        return 2 * math.pi * self.params.inner_rad * angular_fraction

    @cached_property
    def state_qi(self):
        """Where the first clothoid intersects the inner circle (l/r-turn)"""
        st = self.params.state_qi
        st.y *= self.dir
        st.theta *= self.dir
        st.kappa *= self.dir
        return st

    @cached_property
    def _state_qj(self):
        """Where the inner circle segment intersects the second clothoid (left-turn)"""

        ang = self.delta - self.params.delta_min/2
        x = self.params.omega[0] + self.params.inner_rad * np.sin(ang)
        y = self.params.omega[1] - self.params.inner_rad * np.cos(ang)
        kappa = self.params.kappa_max

        return State(x, y, ang, kappa)

    @cached_property
    def state_qj(self):
        """Where the inner circle segment intersects the second clothoid (l/r-turn)"""
        st = self._state_qj
        st.y *= self.dir
        st.theta *= self.dir
        st.kappa *= self.dir
        return st

    @cached_property
    def state_qg(self):
        """The end of the second clothoid (turn left | right for dir=1 | -1)"""
        st = self._state_qg
        st.y *= self.dir
        st.theta *= self.dir
        st.kappa *= self.dir
        return st

    @cached_property
    def _state_qg(self):
        """The end of the second clothoid (left-turn)"""

        st = State(-self.params.omega[0], -self.params.omega[1], self.delta, 0)
        st = st.rotate_then_translate(self.delta + 2 * self.params.gamma, self.params.omega[0], self.params.omega[1])

        return st

