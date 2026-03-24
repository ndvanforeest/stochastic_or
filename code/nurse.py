import numpy as np
import matplotlib.pyplot as plt
from latex_figures import apply_figure_settings
from enum import Enum, auto

apply_figure_settings(use=True)


class State(Enum):
    A_TO_B = auto()
    B_TO_A = auto()
    AT_A = auto()
    AT_B = auto()


rng = np.random.default_rng(3)
thres_A, thres_B = 40, 10

num_weeks = 100
a1 = rng.poisson(3, size=num_weeks)
a2 = rng.poisson(4, size=num_weeks)
c1 = rng.poisson(7, size=num_weeks)
c2 = rng.poisson(8, size=num_weeks)

LA = np.zeros(num_weeks)
LB = np.zeros(num_weeks)
LA[0], LB[0] = 30, 50

p = np.zeros(num_weeks, dtype='object')  # production state
p[0] = State.AT_A

for k in range(1, num_weeks):
    if p[k - 1] == State.AT_A and LA[k - 1] <= thres_A:
        p[k] = State.A_TO_B
    elif p[k - 1] == State.A_TO_B:
        p[k] = State.AT_B
    elif p[k - 1] == State.AT_B and LB[k - 1] <= thres_B:
        p[k] = State.B_TO_A
    elif p[k - 1] == State.B_TO_A:
        p[k] = State.AT_A
    else:  # don't change
        p[k] = p[k - 1]

    d1 = min(LA[k - 1] + a1[k], c1[k] * (p[k] == State.AT_A))
    d2 = min(LB[k - 1] + a2[k], c2[k] * (p[k] == State.AT_B))
    LA[k] = LA[k - 1] + a1[k] - d1
    LB[k] = LB[k - 1] + a2[k] - d2


# Convert cm → inches for Matplotlib
cm_to_inch = 1 / 2.54
fig_width = 6 * cm_to_inch
fig_height = 5.5 * cm_to_inch

xx = range(num_weeks)
plt.figure(figsize=(fig_width, fig_height))
plt.step(xx, LA, ls=":", lw=0.7, where="pre", label="LA")
plt.step(xx, LB, ls=":", lw=0.7, where="pre", label="LB")
plt.xlabel('Time')
plt.legend()
plt.tight_layout()
plt.savefig("../figures/nurse.png", dpi=300)
