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
import random
from unittest import TestCase

import math

import numpy as np

from scc import PathType
from scc import SccPathVariant
from scc import State
from scc import TurnParams
from scc.scc_path_variant import ALL_PATHOPTIONS

NUM_RANDOM_RUNS = 500


class TestPathVariant(TestCase):

    @staticmethod
    def build_valid_random_setup():
        valid = False
        while not valid:
            XPOS1 = random.uniform(-10, 10)
            YPOS1 = random.uniform(-10, 10)
            ANG1 = random.uniform(0, 2*math.pi)
            XPOS2 = random.uniform(-10, 10)
            YPOS2 = random.uniform(-10, 10)
            ANG2 = random.uniform(0, 2*math.pi)

            KAPPA_MAX = random.uniform(0.1, 5)
            SIGMA_MAX = random.uniform(0.1, 5)

            pos1 = State(XPOS1, YPOS1, ANG1, 0)
            pos2 = State(XPOS2, YPOS2, ANG2, 0)
            tparam = TurnParams(KAPPA_MAX, SIGMA_MAX)

            if math.sqrt((XPOS1-XPOS2)**2 + (YPOS1-YPOS2)**2) > 4*tparam.outer_rad:
                valid = True

        return pos1, pos2, tparam

    def test_random_paths(self):

        for i in range(NUM_RANDOM_RUNS):

            pos1, pos2, tparam = self.build_valid_random_setup()

            paths = [SccPathVariant(tparam, pos1, pos2, variant) for variant in
                     ALL_PATHOPTIONS]

            for p in paths:

                states = p.state(np.array([0.0, p.len]))

                self.assertAlmostEqual(states.x[0], pos1.x)
                self.assertAlmostEqual(states.y[0], pos1.y)
                self.assertAlmostEqual(states.theta[0], pos1.theta)
                self.assertAlmostEqual(states.kappa[0], 0.0)

                self.assertAlmostEqual(states.x[1], pos2.x)
                self.assertAlmostEqual(states.y[1], pos2.y)
                self.assertAlmostEqual(states.theta[1], pos2.theta)
                self.assertAlmostEqual(states.kappa[1], 0.0)

    # TODO: straight path: left, right, top bottom

    # TODO: Straight path: diagonal

    # TODO: Force first or second path to be zero-turn!

    # TODO: 90° Turns


