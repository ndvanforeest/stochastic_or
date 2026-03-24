import numpy as np
import matplotlib.pyplot as plt

def initialize_plots():
    import seaborn as sns

    rc = {
        "text.usetex": True,
        "font.family": "fourier",
        "axes.labelsize": 10,
        "font.size": 10,
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
    }
    sns.set(style="whitegrid", rc=rc)


initialize_plots()

num_periods = 10
num_patients = 50
rng = np.random.default_rng(2)

X = rng.uniform(low=0.9, high=1.1, size=(num_patients, num_periods + 1))
X[:, 0] = 0  # set first column of X to 0
A = X.cumsum(axis=1)

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(6, 3))
ax1, ax2, ax3, ax4 = axes.flatten()

ax1.set_xlim(0, 11)
for i in range(num_patients):
    x = A[i, 1:]
    y = i * np.ones(num_periods)
    ax1.plot(x, y, ls='None', marker="o", ms=0.2, c="k")

for i in range(num_patients):
    x = A[i, 1:]
    y = rng.uniform(-0.5, 0.5, size=num_periods)  # add jitter
    ax1.plot(x, y, ls='None', marker="o", ms=0.2, c="k")

A = np.sort(A.flatten())
X = A[1:] - A[:-1]

bins = np.linspace(0, 5 / num_patients, 50)
exp_density = num_patients * np.exp(-num_patients * bins)
ax2.hist(X, bins, density=True, color="k")
ax2.plot(bins, exp_density, ":", c="k", lw=0.75, label="pdf")
ax2.legend()

X = rng.uniform(low=0.9, high=1.1, size=(num_patients, num_periods + 1))
X[:, 0] = rng.uniform(low=0, high=1, size=num_patients)
A = X.cumsum(axis=1)

ax3.set_xlim(0, 11)

for i in range(num_patients):
    x = A[i, 1:]
    y = i * np.ones(num_periods)
    ax3.plot(x, y, ls='None', marker="o", ms=0.2, c="k")

for i in range(num_patients):
    x = A[i, 1:]
    y = rng.uniform(-0.5, 0.5, size=num_periods)  # add jitter
    ax3.plot(x, y, ls='None', marker="o", ms=0.2, c="k")

A = np.sort(A.flatten())
X = A[1:] - A[:-1]
bins = np.linspace(0, 5 / num_patients, 50)
ax4.hist(X, bins, density=True, color="k")
exp_density = num_patients * np.exp(-num_patients * bins)
ax4.plot(bins, exp_density, ":", c="k", lw=0.75, label="pdf")
ax4.legend()

fig.tight_layout()
fig.savefig("../figures/IBD_exponential.pdf")
fig.savefig("../figures/IBD_exponential.png", dpi=300)
