import numpy as np
from scipy.stats import bernoulli
import matplotlib.pylab as plt

from latex_figures import apply_figure_settings

apply_figure_settings(use=True)

np.random.seed(3)

n = 30
a = bernoulli(0.3).rvs(n)
a[0] = 0
s = bernoulli(0.4).rvs(n)
z = a.cumsum() - s.cumsum()  # z is the random walk
zmin = np.minimum.accumulate(z)
q = z - zmin  # reflection

# Convert cm → inches for Matplotlib
cm_to_inch = 1 / 2.54
fig_width = 6 * cm_to_inch
fig_height = 5.5 * cm_to_inch

fig = plt.figure(figsize=(fig_width, fig_height))
plt.plot(z, 'o-', markersize=2, ls=":", lw=0.5, label="Z")
plt.plot(q, 'o-', markersize=2, ls=":", lw=0.5, label='L')
plt.xlabel('Time')
plt.legend(loc='lower left')

plt.tight_layout()
plt.savefig("../figures/random_walk1.png", dpi=300, bbox_inches='tight')


# make a random walk with steps up and down.
a = 2 * bernoulli(0.49).rvs(n) - 1
a[0] = 0
z = a.cumsum()
zmin = np.minimum.accumulate(z)
q = z - zmin

fig = plt.figure(figsize=(fig_width, fig_height))
plt.plot(z, 'o-', markersize=2, ls=":", lw=0.5, label="Z")
plt.plot(q, 'o-', markersize=2, ls=":", lw=0.5, label='L')

plt.xlabel('Time')
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig("../figures/random_walk2.png", dpi=300, bbox_inches='tight')
