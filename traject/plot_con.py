"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""
import random

import numpy as np
import matplotlib.pyplot as plt
import math

# Create a figure of size 8x6 inches, 80 dots per inch
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

from traject.scc import State
from traject.scc import Turn
from traject.scc.scc_path_variant import SccPathVariant
from traject.scc.turnparams import TurnParams

# Create a new subplot from a grid of 3x3
gs = GridSpec(3, 3)
fig = plt.figure(figsize=(8, 14))
ax0 = fig.add_subplot(gs[:, :])
ax0.set_label("x-y")


XPOS = random.uniform(-10, 10)
YPOS = random.uniform(-10, 10)
ANG  = random.uniform(-math.pi, math.pi)
print(" ANG="+str(ANG))

pos1 = State(0, 0, 0, 0)
pos2 = State(XPOS, YPOS, ANG, 0)
tparam = TurnParams(1.0, 1.0)
sccp = SccPathVariant(tparam, pos1, pos2)


# omil
ax0.add_patch(Circle(sccp.om1l, tparam.outer_rad, facecolor='none', edgecolor='black'))
ax0.add_patch(Circle(sccp.om1l, tparam.inner_rad, facecolor='none', edgecolor='black'))
ax0.plot(sccp.om1l[0], sccp.om1l[1], "go")
ax0.text(sccp.om1l[0], sccp.om1l[1], "om1l")
# omir
#ax0.add_patch(Circle(sccp.om1r, tparam.outer_rad, facecolor='none', edgecolor='black'))
#ax0.add_patch(Circle(sccp.om1r, tparam.inner_rad, facecolor='none', edgecolor='black'))
ax0.plot(sccp.om1r[0], sccp.om1r[1], "go")
ax0.text(sccp.om1r[0], sccp.om1r[1], "om1r")


# om2r
ax0.add_patch(Circle(sccp.om2r, tparam.outer_rad, facecolor='none', edgecolor='black'))
ax0.add_patch(Circle(sccp.om2r, tparam.inner_rad, facecolor='none', edgecolor='black'))
ax0.plot(sccp.om2r[0], sccp.om2r[1], "go")
ax0.text(sccp.om2r[0], sccp.om2r[1], "om2r")
# om2l
ax0.plot(sccp.om2l[0], sccp.om2l[1], "go")
ax0.text(sccp.om2l[0], sccp.om2l[1], "om2l")


# Set x limits, ticks, etc.
#ax0.set_xlim(-2.0, XPOS+2)
#ax0.set_ylim(-2.0, YPOS+2)

# plot first arc
#X = np.linspace(0, sccp.lsr_turn1.len, 128, endpoint=True)
#tra = sccp.lsr_turn1.state(X)
#ax0.plot(tra.x, tra.y, color="yellow", linewidth=5.0, linestyle="-")

# plot second arc
#X = np.linspace(0, sccp._lsr_turn2.len, 128, endpoint=True)
#tra = sccp._state_turn2(X)
#ax0.plot(tra.x, tra.y, color="yellow", linewidth=5.0, linestyle="-")

# connection line:
qg1 = sccp.lsr_q1
qg2 = sccp.lsr_q2
ax0.add_line(Line2D([qg1.x, qg2.x], [qg1.y, qg2.y]))

# plot pos2:
ax0.plot(pos2.x, pos2.y, "bx")

# plot the whole thing:
X = np.linspace(0, sccp.len, 128, endpoint=True)
tra = sccp.state(X)
ax0.plot(tra.x, tra.y, color="yellow", linewidth=5.0, linestyle="-")

print("lsr_om12_ang: "+str(sccp.lsr_om12_ang))
print("turn2_ang: "+str(sccp.turn2_ang))

# Show result on screen
plt.show()

