"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# Create a figure of size 8x6 inches, 80 dots per inch
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle

from traject.scc import State
from traject.scc import Turn
from traject.scc.connection import Connection
from traject.scc.turnparams import TurnParams

# Create a new subplot from a grid of 3x3
gs = GridSpec(3, 3)
fig = plt.figure(figsize=(8, 14))
ax0 = fig.add_subplot(gs[:, :])
ax0.set_label("x-y")


pos1 = State(0, 0, 0, 0)
pos2 = State(4, 3, 0, 0)
tparam = TurnParams(1.0, 1.0)
conn = Connection(tparam, pos1, pos2)


ax0.add_patch(Circle(conn.om1l, tparam.outer_rad, facecolor='none', edgecolor='black'))
ax0.plot(conn.om1l[0], conn.om1l[1], "go")

ax0.add_patch(Circle(conn.om2r, tparam.outer_rad, facecolor='none', edgecolor='black'))
ax0.plot(conn.om2r[0], conn.om2r[1], "go")

# Set x limits, ticks, etc.
ax0.set_xlim(-1.0, 5.0)
ax0.set_ylim(-1.0, 4.0)

alpha2 = conn.lsr_alpha2
turn = Turn(tparam, alpha2)
# plot whole line
X = np.linspace(0, turn.len, 128, endpoint=True)
tra = turn.state(X)
ax0.plot(tra.x, tra.y, color="yellow", linewidth=5.0, linestyle="-")


# Show result on screen
plt.show()
