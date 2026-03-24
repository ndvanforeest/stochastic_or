import numpy as np
import matplotlib.pyplot as plt
from latex_figures import apply_figure_settings

apply_figure_settings(use=True)

rng = np.random.default_rng(3)

num_weeks = 100
a = rng.poisson(1, size=num_weeks)
c = rng.poisson(5, size=num_weeks)
N = 20

L = np.zeros(num_weeks)
I = np.zeros(num_weeks)  # on or not

for k in range(1, num_weeks):
    I[k] = (L[k - 1] >= N) + I[k - 1] * (0 < L[k - 1] < N)
    c[k] *= I[k]
    d = min(L[k - 1] + a[k], c[k])
    L[k] = L[k - 1] + a[k] - d


cm_to_inch = 1 / 2.54
fig_width = 6 * cm_to_inch
fig_height = 5.5 * cm_to_inch
xx = range(num_weeks)
plt.figure(figsize=(fig_width, fig_height))
plt.step(xx, L, ":", lw=0.7, where="pre", label="L")
plt.step(xx, 30 * I, "-", ms=0.5, lw=0.4, where="pre", label="I")
plt.xlabel('Time')
plt.legend()
plt.tight_layout()
plt.savefig("../figures/N-policy.png", dpi=300)
