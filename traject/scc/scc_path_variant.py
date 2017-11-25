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
    def turn1_ang(self):
        return self.lsr_q12_ang - self.st1.theta

    @cached_property
    def turn2_ang(self):
        return self.lsr_q12_ang - self.st2.theta       # going backwards!

    @cached_property
    def lsr_turn1(self):
        return Turn(self.params, self.turn1_ang)

    @cached_property
    def lsr_turn2(self):
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
        qg2 = self.lsr_turn1.state_qg.rotate_then_translate(self.st2.theta+math.pi, self.st2.x, self.st2.y)
        return qg2

    def state_turn2(self, s):
        return self.lsr_turn2.state(s).rotate_then_translate(self.st2.theta + math.pi, self.st2.x, self.st2.y)
