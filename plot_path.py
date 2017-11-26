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
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from scc import State
from scc.scc_path_variant import SccPathVariant, PathType

from scc.turnparams import TurnParams

# Create a new subplot from a grid of 3x3
gs = GridSpec(3, 3)
fig = plt.figure(figsize=(8, 14))
ax0 = fig.add_subplot(gs[:-1, :])
ax0.set_label("x-y")
ax1 = fig.add_subplot(gs[-1, :])
ax1.set_label("s-theta")


XPOS1 = random.uniform(-10, 10)
YPOS1 = random.uniform(-10, 10)
ANG1  = random.uniform(-math.pi, math.pi)
XPOS2 = random.uniform(-10, 10)
YPOS2 = random.uniform(-10, 10)
ANG2  = random.uniform(-math.pi, math.pi)
PATHOPTIONS = [PathType.lsl, PathType.rsr, PathType.rsl, PathType.lsr]

#KAPPA_MAX = random.uniform(0.1, 5)
#SIGMA_MAX = random.uniform(0.1, 5)
KAPPA_MAX = SIGMA_MAX = 1


print("  ANG1      = " + str(ANG1))
print("  ANG2      = " + str(ANG2))
print("  KAPPA_MAX = " + str(KAPPA_MAX))
print("  SIGMA_MAX = " + str(SIGMA_MAX))

pos1 = State(XPOS1, YPOS1, ANG1, 0)
pos2 = State(XPOS2, YPOS2, ANG2, 0)
tparam = TurnParams(KAPPA_MAX, SIGMA_MAX)

paths = [SccPathVariant(tparam, pos1, pos2, variant) for variant in
         PATHOPTIONS]
shortest_path = min(paths, key=lambda path: path.len)

print("Shortest path type: "+str(shortest_path.ptype))

for p in paths:
    print("  PT: "+str(p.ptype)+" len: "+str(p.len))

# plot the whole thing:
for p in paths:
    X = np.linspace(0, p.len, 128, endpoint=True)
    tra = p.state(X)
    ax0.plot(tra.x, tra.y, color="yellow", linewidth=5.0, linestyle="-")

# plot the winner again:
X = np.linspace(0, shortest_path.len, 128, endpoint=True)
tra = shortest_path.state(X)
ax0.plot(tra.x, tra.y, color="green", linewidth=1.0, linestyle="--")

# omil
ax0.add_patch(Circle(shortest_path.om1l, tparam.outer_rad, facecolor='none', edgecolor='black'))
ax0.add_patch(Circle(shortest_path.om1l, tparam.inner_rad, facecolor='none', edgecolor='black'))
ax0.plot(shortest_path.om1l[0], shortest_path.om1l[1], "go")
ax0.text(shortest_path.om1l[0], shortest_path.om1l[1], "om1l")
# omir
#ax0.add_patch(Circle(sccp.om1r, tparam.outer_rad, facecolor='none', edgecolor='black'))
#ax0.add_patch(Circle(sccp.om1r, tparam.inner_rad, facecolor='none', edgecolor='black'))
ax0.plot(shortest_path.om1r[0], shortest_path.om1r[1], "go")
ax0.text(shortest_path.om1r[0], shortest_path.om1r[1], "om1r")


# om2r
ax0.add_patch(Circle(shortest_path.om2r, tparam.outer_rad, facecolor='none', edgecolor='black'))
ax0.add_patch(Circle(shortest_path.om2r, tparam.inner_rad, facecolor='none', edgecolor='black'))
ax0.plot(shortest_path.om2r[0], shortest_path.om2r[1], "go")
ax0.text(shortest_path.om2r[0], shortest_path.om2r[1], "om2r")
# om2l
ax0.plot(shortest_path.om2l[0], shortest_path.om2l[1], "go")
ax0.text(shortest_path.om2l[0], shortest_path.om2l[1], "om2l")

# connection line:
qg1 = shortest_path.q1
qg2 = shortest_path.q2
ax0.add_line(Line2D([qg1.x, qg2.x], [qg1.y, qg2.y]))

# plot pos1:
ax0.plot(pos1.x, pos1.y, "bo")
# plot pos2:
ax0.plot(pos2.x, pos2.y, "bx")

print("lsr_om12_ang: " + str(shortest_path.om12_ang))
print("turn2_ang: " + str(shortest_path.turn2_ang))

# plot theta, kappa:
ax1.plot(X, tra.x, color="green", linewidth=1.0, linestyle="-", label="x")
ax1.plot(X, tra.y, color="blue", linewidth=1.0, linestyle="-", label="y")
ax1.plot(X, tra.theta, color="black", linewidth=1.0, linestyle="-", label="theta")
ax1.plot(X, tra.kappa, color="red", linewidth=1.0, linestyle="-", label="kappa")
ax1.legend()



# Show result on screen
plt.show()

