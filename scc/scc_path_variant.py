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
from enum import Enum

import numpy as np
from property_manager import cached_property

from scc import Turn
from scc.helpers import calc_ang
from .state import State
from .turnparams import TurnParams


class PathType(Enum):
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
    def __init__(self, params, st1, st2, ptype):
        """

        Parameters
        ----------
        st1 : State
        st2 : State
        params : TurnParams
        ptype : PathType
            The path type
        """
        self.st1 = st1
        self.st2 = st2
        self.params = params
        self.ptype = ptype

        assert(self.om12_dist > 2 * self.params.outer_rad)

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
    def om1(self):
        if self.ptype in [PathType.lsl, PathType.lsr, PathType.lrl]:
            return self.om1l
        else:
            return self.om1r

    @cached_property
    def om2(self):
        if self.ptype in [PathType.lsl, PathType.rsl, PathType.lrl]:
            return self.om2l
        else:
            return self.om2r

    @cached_property
    def om12_dist(self):
        dx = self.om2[0] - self.om1[0]
        dy = self.om2[1] - self.om1[1]
        dist = math.sqrt(dx**2 + dy**2)
        return dist

    @cached_property
    def om12_ang(self):
        dx = self.om2[0] - self.om1[0]
        dy = self.om2[1] - self.om1[1]
        return calc_ang(dx, dy)

    @cached_property
    def alpha2(self):
        gamma = self.params.gamma
        rt = self.params.outer_rad
        alpha2 = math.asin(2 * math.cos(gamma) * rt / self.om12_dist)
        return alpha2

    @cached_property
    def q12_ang(self):
        if self.ptype == PathType.rsl:
            return self.om12_ang - self.alpha2
        elif self.ptype == PathType.lsr:
            return self.om12_ang + self.alpha2
        elif self.ptype in [PathType.lsl, PathType.rsr]:
            return self.om12_ang
        return None

    @cached_property
    def q12_len(self):
        dx = self.q2.x - self.q1.x
        dy = self.q2.y - self.q1.y
        return math.sqrt(dx*dx + dy*dy)

    @cached_property
    def turn1_ang(self):
        ang = self.q12_ang - self.st1.theta
        if self.ptype in [PathType.lsl, PathType.lsr, PathType.lrl]:
            return ang % (2*math.pi)                    # left turn: make angle positive
        else:
            return ang % (2*math.pi) - 2*math.pi        # right turn: make angle negative

    @cached_property
    def turn2_ang(self):
        """The direction of the second turn should be considered from the rear end,
           such that a positive turn angle makes a right turn!"""
        ang = self.q12_ang - self.st2.theta
        if self.ptype in [PathType.lsr, PathType.rsr, PathType.rlr]:
            return ang % (2*math.pi)                    # right turn: make angle positive
        else:
            return ang % (2*math.pi) - 2*math.pi        # left turn: make angle negative

    @cached_property
    def turn1(self):
        """ get the Turn object for the first turn
        Returns
        -------
        Turn
        """
        return Turn(self.params, self.turn1_ang)

    @cached_property
    def _turn2(self):
        """
        The second turn will be used from the rear end!
        """
        return Turn(self.params, self.turn2_ang)

    @cached_property
    def q1(self):
        qg1 = self.turn1.state_qg.rotate_then_translate(self.st1.theta, self.st1.x, self.st1.y)
        return qg1

    @cached_property
    def q2(self):
        qg2 = self._turn2.state_qg.rotate_then_translate(self.st2.theta + math.pi, self.st2.x, self.st2.y)
        return qg2

    def _state_turn2(self, s):
        # map s from [len_total-len_arc2 .. len_total] to [len_arc2 .. 0]
        my_s = - (s - self.len)
        return self._turn2.state(my_s).rotate_then_translate(self.st2.theta + math.pi, self.st2.x, self.st2.y)

    def _state_straight(self, s):
        # map s from [len_arc1 .. len_arc1+lsr_q12_len] to [0 .. 1]
        my_s = (s - self.turn1.len) / self.q12_len
        dx = self.q2.x - self.q1.x
        dy = self.q2.y - self.q1.y

        x = self.q1.x + dx * my_s
        y = self.q1.y + dy * my_s
        theta = np.full(len(s), self.q1.theta)
        kappa = np.zeros(len(s))

        return State(x, y, theta, kappa)

    @cached_property
    def len(self):
        return self.turn1.len + self._turn2.len + self.q12_len

    def state(self, s):
        x = np.empty(len(s))
        y = np.empty(len(s))
        theta = np.empty(len(s))
        kappa = np.empty(len(s))

        arc1_cond = s < self.turn1.len
        straight_cond = (s > self.turn1.len) & \
                        (s < self.turn1.len + self.q12_len)
        arc2_cond = s > self.turn1.len + self.q12_len

        # arc 1
        arc1 = self.turn1.state(s[arc1_cond])
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
