"""
    Copyright: Gerd Gruenert, 2017
    All rights reserved.
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# Create a figure of size 8x6 inches, 80 dots per inch
import scipy.special
from matplotlib.patches import Circle

from traject.scc.turn import Turn
from traject.scc.turnparams import TurnParams

# Create a new subplot from a grid of 1x1
fig, ax = plt.subplots(figsize=(8, 8))


tparam = TurnParams(1.0, 1.0)
turn = Turn(tparam, math.pi*0.9, 1)

# plot outer circle:
omega = tparam.omega
ax.add_patch(Circle(omega, tparam.outer_rad, facecolor='none', edgecolor='black'))

# plot inner circle center point:
ax.add_patch(Circle(omega, tparam.inner_rad))
plt.plot(omega[0], omega[1], "x", color='black')

# plot whole line
XT = np.linspace(0, turn.len, 128, endpoint=True)
tra = turn.state(XT)
plt.plot(tra.x, tra.y, color="yellow", linewidth=5.0, linestyle="-")


# plot arc segment
X = np.linspace(0, tparam.len_clothoid_part, 128, endpoint=True)
tra = turn.state_clothoid_first(X)
plt.plot(tra.x, tra.y, color="red", linewidth=1.0, linestyle="-")

# plot circle arc segment:
X2 = np.linspace(tparam.len_clothoid_part, tparam.len_clothoid_part+turn.len_of_circular_part, 128, endpoint=True)
tra = turn.state_circular(X2)
plt.plot(tra.x, tra.y, color="cyan", linewidth=2.0, linestyle="-")

# plot qi point:
plt.plot(tparam.state_qi.x, tparam.state_qi.y, "go")

# plot qj point:
plt.plot(turn.state_qj.x, turn.state_qj.y, "ro")

# plot qg point:
plt.plot(turn.state_qg.x, turn.state_qg.y, "bo")

# plot second clothoid:
X3 = np.linspace(tparam.len_clothoid_part+turn.len_of_circular_part, 2*tparam.len_clothoid_part+turn.len_of_circular_part, 128, endpoint=True)
tra = turn.state_clothoid_second(X3)
plt.plot(tra.x, tra.y, color="red", linewidth=1.0, linestyle="-")

# Set x limits, ticks, etc.
plt.xlim(-4.0, 4.0)
plt.xticks(np.linspace(-4, 4, 9, endpoint=True))
plt.ylim(-4.0, 4.0)
plt.yticks(np.linspace(-4, 4, 9, endpoint=True))

# Save figure using 72 dots per inch
# plt.savefig("exercice_2.png", dpi=72)

# Show result on screen
plt.show()
