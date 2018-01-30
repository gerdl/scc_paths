
Simple Continuous Curvature Path Library in Python
==================================================

This library implements the calculation of
simple continuous curvature paths as described
by the paper of Scheuer and Fraichard in python:

    @inproceedings{scheuer1997continuous,
      title={Continuous-curvature path planning for car-like vehicles},
      author={Scheuer, Alexis and Fraichard, Thierry},
      booktitle={Intelligent Robots and Systems, 1997. IROS'97., Proceedings of the 1997 IEEE/RSJ International Conference on},
      volume={2},
      pages={997--1003},
      year={1997},
      organization={IEEE}
    }

License
-------

GPLv3 - please contact me if you need the software under a different license.


Example use - single Turn
-------------------------

### input ###

kappa_max = Max curvature == 1/r of the inner curve radius r

sigma_max = The steering rate, i.e., the sharpness of the turn

### output ###

Static Turn info:

    Turn.len = Length of the complete turn
    Turn.len_of_circular_part
    Turn.state_qg = Endpoint of the turn

State:  (sequence of trajectory points)

    x, y = positions
    theta = angle
    kappa = curvature == 1/r of the curve radius

### use ###

```python
import numpy as np
from scc.turn import Turn
from scc.turnparams import TurnParams

# set parameters:
tparam = TurnParams(_kappa_max=1.8,
                    _sigma_max=1.0)

# setup a single turn:
turn = Turn(_params=tparam, _delta=math.pi*0.76)

# calculate a set of trajectory points:
XT = np.linspace(0, turn.len, 128, endpoint=True)
tra = turn.state(XT)
print (tra.x)
print (tra.y)
```


Or more complete: `plot_curve.py`

![alt text][example_images/plot_curve.png]


Example use - Scc Path
----------------------

```python
import numpy as np
from scc.turn import Turn
from scc.turnparams import TurnParams

# set parameters:
pos1 = State(_x=-3.0, _y=6.4, _theta=math.pi*0.7, _kappa=0)
pos1 = State(_x=10.0, _y=8.2, _theta=math.pi*0.55, _kappa=0)
tparam = TurnParams(_kappa_max=1.8,
                    _sigma_max=1.0)

PATHOPTIONS = [PathType.lsl, PathType.rsr, PathType.rsl, PathType.lsr]
paths = [SccPathVariant(tparam, pos1, pos2, variant) for variant in
         PATHOPTIONS]
shortest_path = min(paths, key=lambda path: path.len)

# calculate positions:
X = np.linspace(0, shortest_path.len, 128, endpoint=True)
tra = shortest_path.state(X)
print (tra.x)
print (tra.y)
```

Or more complete: `plot_path.py`

![alt text][example_images/plot_path.png]
