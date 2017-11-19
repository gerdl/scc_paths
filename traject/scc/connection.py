"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""
import math

from property_manager import cached_property

from .state import State
from .turnparams import TurnParams


class Connection(object):
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
    def om2r(self):
        """Omega_2, for a right turn"""

        # starting from the other end, it's a left turn, too:
        om = self.params.omega
        theta = (self.st2.theta + math.pi) % (2*math.pi)

        st = State(om[0], om[1], 0, 0).rotate_then_translate(theta, self.st2.x, self.st2.y)
        return st.x, st.y

    @cached_property
    def lsr_om1om2_dist(self):
        dx = self.om2r[0] - self.om1l[0]
        dy = self.om2r[1] - self.om1l[1]
        dist = math.sqrt(dx**2 + dy**2)
        return dist

    @cached_property
    def lsr_alpha2(self):
        gamma = self.params.gamma
        rt = self.params.outer_rad
        alpha2 = math.asin( 2*math.cos(gamma)*rt / self.lsr_om1om2_dist)
        return alpha2

