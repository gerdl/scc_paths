"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""

import math

from property_manager import cached_property

import scipy.special


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

    def state(self, time):
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
            time : float

        """
        pass

    def state_circular(self, time):
        pass

    def state_clothoid_first(self, time):
        """
        Parameters
        ----------
        time : float
        """
        assert(time >= 0)
        assert(time <= self.params.delta_min / 2)

        scale = math.sqrt(math.pi / self.params.sigma_max)

        xy = scale * scipy.special.fresnel(math.sqrt())
        theta =
        kappa =


    @cached_property
    def len_of_turn(self):
        pass

    def len_of_circular_part(self):

        theta_circ = self.delta - self.params.delta_min


