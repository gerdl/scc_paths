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
import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle
from scc.turn import Turn

from scc.turnparams import TurnParams

KAPPA_MAX = random.uniform(0.1, 5)
SIGMA_MAX = random.uniform(0.1, 5)
DELTA = random.uniform(-2*math.pi, 2*math.pi)
print("  DELTA is     "+str(DELTA))
print("  KAPPA_MAX is "+str(KAPPA_MAX))
print("  SIGMA_MAX is "+str(SIGMA_MAX))

# Create a new subplot from a grid of 3x3
gs = GridSpec(3, 3)
fig = plt.figure(figsize=(8, 14))
ax0 = fig.add_subplot(gs[:-1, :])
ax0.set_label("x-y")

ax1 = fig.add_subplot(gs[-1, :])
ax1.set_label("s-theta")


tparam = TurnParams(KAPPA_MAX, SIGMA_MAX)
turn = Turn(tparam, DELTA)

# plot outer circle:
omega = tparam.omega
ax0.add_patch(Circle(omega, tparam.outer_rad, facecolor='none', edgecolor='black'))

# plot inner circle center point:
ax0.add_patch(Circle(omega, tparam.inner_rad))
ax0.plot(omega[0], omega[1], "x", color='black')

# plot whole line
XT = np.linspace(0, turn.len, 128, endpoint=True)
tra = turn.state(XT)
ax0.plot(tra.x, tra.y, color="yellow", linewidth=5.0, linestyle="-")

# plot arc segment
X = np.linspace(0, tparam.len_clothoid_part, 128, endpoint=True)
tra = turn._state_clothoid_first(X)
ax0.plot(tra.x, tra.y, color="red", linewidth=1.0, linestyle="-")

# plot circle arc segment:
if turn.delta > tparam.delta_min:
    X2 = np.linspace(tparam.len_clothoid_part, tparam.len_clothoid_part+turn.len_of_circular_part, 128, endpoint=True)
    tra = turn._state_circular(X2)
    ax0.plot(tra.x, tra.y, color="cyan", linewidth=2.0, linestyle="-")

# plot qi point:
ax0.plot(turn.state_qi.x, turn.state_qi.y, "go")

# plot qj point:
ax0.plot(turn.state_qj.x, turn.state_qj.y, "ro")

# plot qg point:
ax0.plot(turn.state_qg.x, turn.state_qg.y, "bo")

# plot second clothoid:
X3 = np.linspace(tparam.len_clothoid_part+turn.len_of_circular_part, 2*tparam.len_clothoid_part+turn.len_of_circular_part, 128, endpoint=True)
tra = turn._state_clothoid_second(X3)
ax0.plot(tra.x, tra.y, color="red", linewidth=1.0, linestyle="-")

# Set x limits, ticks, etc.
#ax0.set_xlim(-4.0, 4.0)
#ax0.set_xticks(np.linspace(-4, 4, 9, endpoint=True))
#ax0.set_ylim(-4.0, 4.0)
#ax0.set_yticks(np.linspace(-4, 4, 9, endpoint=True))


# -----------------------------------
# plot whole line
XT = np.linspace(0, turn.len, 128, endpoint=True)
# turn = Turn(tparam, DELTA)
tra = turn.state(XT)
ax1.plot(XT, tra.x, color="green", linewidth=1.0, linestyle="-", label="x")
ax1.plot(XT, tra.y, color="blue", linewidth=1.0, linestyle="-", label="y")
ax1.plot(XT, tra.theta, color="black", linewidth=1.0, linestyle="-", label="theta")
ax1.plot(XT, tra.kappa, color="red", linewidth=1.0, linestyle="-", label="kappa")
ax1.legend()

# plot again to chaeck we didn't accidentally change something
# ax0.plot(tra.x, tra.y, color="cyan", linewidth=5.0, linestyle="-")


# Show result on screen
plt.show()
