"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""
import math

from property_manager import cached_property

from traject.scc import Turn
from traject.scc.helpers import calc_ang
from .state import State
from .turnparams import TurnParams

from enum import Enum
import numpy as np

class SccType(Enum):
    lsl = 1,
    rsr = 2,
    lsr = 3,
    rsl = 4,
    rlr = 5,
    lrl = 6


class SccPathVariant(object):
    """
    Turn types:
        lsl, rsr, lsr, rsl, rlr, lrl
    """
    def __init__(self, params, st1, st2):
        """

        Parameters
        ----------
        st1 : State
        st2 : State
        params : TurnParams
        """
        self.st1 = st1
        self.st2 = st2
        self.params = params

        assert(self.lsr_om12_dist > 2*self.params.outer_rad)

    def lsr(self, s):

        # om1 = left turn
        om1 = self.params.omega

        # om1 = right turn
        om2 = self.params.omega_r

    @cached_property
    def om1l(self):
        """Omega_1, for a left turn"""
        om = self.params.omega
        st = State(om[0], om[1], 0, 0).rotate_then_translate(self.st1.theta, self.st1.x, self.st1.y)
        return st.x, st.y

    @cached_property
    def om1r(self):
        """Omega_1, for a right turn"""
        om = self.params.omega
        st = State(om[0], -om[1], 0, 0).rotate_then_translate(self.st1.theta, self.st1.x, self.st1.y)
        return st.x, st.y

    @cached_property
    def om2r(self):
        """Omega_2, for a right turn"""

        # starting from the other end, it's a left turn, too:
        om = self.params.omega
        theta = (self.st2.theta + math.pi) % (2*math.pi)

        st = State(om[0], om[1], 0, 0).rotate_then_translate(theta, self.st2.x, self.st2.y)
        return st.x, st.y

    @cached_property
    def om2l(self):
        """Omega_2, for a left turn"""

        # starting from the other end, it's a right turn, too:
        om = self.params.omega
        theta = (self.st2.theta + math.pi) % (2*math.pi)

        st = State(om[0], -om[1], 0, 0).rotate_then_translate(theta, self.st2.x, self.st2.y)
        return st.x, st.y

    @cached_property
    def lsr_om12_dist(self):
        dx = self.om2r[0] - self.om1l[0]
        dy = self.om2r[1] - self.om1l[1]
        dist = math.sqrt(dx**2 + dy**2)
        return dist

    @cached_property
    def lsr_om12_ang(self):
        dx = self.om2r[0] - self.om1l[0]
        dy = self.om2r[1] - self.om1l[1]
        return calc_ang(dx, dy)

    @cached_property
    def lsr_alpha2(self):
        gamma = self.params.gamma
        rt = self.params.outer_rad
        alpha2 = math.asin(2 * math.cos(gamma) * rt / self.lsr_om12_dist)
        return alpha2

    @cached_property
    def lsr_q12_ang(self):
        return self.lsr_om12_ang + self.lsr_alpha2

    @cached_property
    def lsr_q12_len(self):
        dx = self.lsr_q2.x - self.lsr_q1.x
        dy = self.lsr_q2.y - self.lsr_q1.y
        return math.sqrt(dx*dx + dy*dy)

    @cached_property
    def turn1_ang(self):
        ang = self.lsr_q12_ang - self.st1.theta
        return ang % (2*math.pi)        # make angle positive

    @cached_property
    def turn2_ang(self):
        ang = self.lsr_q12_ang - self.st2.theta
        return ang % (2*math.pi)        # going backwards, make it positive

    @cached_property
    def lsr_turn1(self):
        """

        Returns
        -------
        Turn
        """
        return Turn(self.params, self.turn1_ang)

    @cached_property
    def _lsr_turn2(self):
        """
        maybe shouldn't be used directly - not yet translated and turned!
        """
        return Turn(self.params, self.turn2_ang)

    @cached_property
    def lsr_q1(self):
        qg1 = self.lsr_turn1.state_qg
        return qg1

    @cached_property
    def lsr_q2(self):
        qg2 = self._lsr_turn2.state_qg.rotate_then_translate(self.st2.theta + math.pi, self.st2.x, self.st2.y)
        return qg2

    def _state_turn2(self, s):

        # map s from [len_total-len_arc2 .. len_total] to [len_arc2 .. 0]
        my_s = - (s - self.len)
        return self._lsr_turn2.state(my_s).rotate_then_translate(self.st2.theta + math.pi, self.st2.x, self.st2.y)

    def _state_straight(self, s):
        # map s from [len_arc1 .. len_arc1+lsr_q12_len] to [0 .. 1]
        my_s = (s - self.lsr_turn1.len) / self.lsr_q12_len
        dx = self.lsr_q2.x - self.lsr_q1.x
        dy = self.lsr_q2.y - self.lsr_q1.y

        x = self.lsr_q1.x + dx * my_s
        y = self.lsr_q1.y + dy * my_s
        theta = np.full(len(s), self.lsr_q1.theta)
        kappa = np.zeros(len(s))

        return State(x, y, theta, kappa)

    @cached_property
    def len(self):
        return self.lsr_turn1.len + self._lsr_turn2.len + self.lsr_q12_len

    def state(self, s):
        x = np.empty(len(s))
        y = np.empty(len(s))
        theta = np.empty(len(s))
        kappa = np.empty(len(s))

        arc1_cond = s < self.lsr_turn1.len
        straight_cond = (s > self.lsr_turn1.len) & \
                        (s < self.lsr_turn1.len + self.lsr_q12_len)
        arc2_cond = s > self.lsr_turn1.len + self.lsr_q12_len

        # arc 1
        arc1 = self.lsr_turn1.state(s[arc1_cond])
        x[arc1_cond] = arc1.x
        y[arc1_cond] = arc1.y
        theta[arc1_cond] = arc1.theta
        kappa[arc1_cond] = arc1.kappa

        # straight segment:
        straight = self._state_straight(s[straight_cond])
        x[straight_cond] = straight.x
        y[straight_cond] = straight.y
        theta[straight_cond] = straight.theta
        kappa[straight_cond] = straight.kappa

        # arc 2
        arc2 = self._state_turn2(s[arc2_cond])
        x[arc2_cond] = arc2.x
        y[arc2_cond] = arc2.y
        theta[arc2_cond] = arc2.theta
        kappa[arc2_cond] = arc2.kappa

        return State(x, y, theta, kappa)
