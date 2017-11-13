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

# X = np.linspace(0, 3/2*np.pi, 500, endpoint=True)
#C, S = scipy.special.fresnel(np.sqrt(2*X/math.pi))

# Plot cosine with a blue continuous line of width 1 (pixels)
#plt.plot(X, C, color="blue", linewidth=1.0, linestyle="-")
# Plot sine with a green continuous line of width 1 (pixels)
#plt.plot(X, S, color="green", linewidth=1.0, linestyle="-")
#plt.plot(C, S, color="red", linewidth=1.0, linestyle="-")



tp = TurnParams(1.0, 1.0)
turn = Turn(tp, math.pi, 1)

# plot outer circle:
omega = tp.omega
ax.add_patch(Circle(omega, tp.outer_rad, facecolor='none', edgecolor='black'))

# plot inner circle center point:
ax.add_patch(Circle(omega, tp.inner_rad))
plt.plot(omega[0], omega[1], "x", color='black')

# plot arc segment
X = np.linspace(0, tp.len_clothoid_part, 500, endpoint=True)
tra = turn.state_clothoid_first(X)
plt.plot(tra[0], tra[1], color="red", linewidth=1.0, linestyle="-")

# plot qi point:
plt.plot(tp.state_qi[0], tp.state_qi[1], "go")

# Set x limits, ticks, etc.
plt.xlim(-4.0, 4.0)
plt.xticks(np.linspace(-4, 4, 9, endpoint=True))
plt.ylim(-4.0, 4.0)
plt.yticks(np.linspace(-4, 4, 9, endpoint=True))

# Save figure using 72 dots per inch
# plt.savefig("exercice_2.png", dpi=72)

# Show result on screen
plt.show()
