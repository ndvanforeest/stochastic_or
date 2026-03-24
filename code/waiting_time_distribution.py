import numpy as np
import matplotlib.pyplot as plt

from functions import Plus
from random_variable import NumericRV as RV

from latex_figures import apply_figure_settings

apply_figure_settings(use=True)

X = RV({3: 1 / 3, 4: 1 / 3, 5: 1 / 3})
S = RV({4: 1 / 3, 5: 1 / 3, 7: 1 / 3})
print(f"{X.mean()=:0.2f}, {S.mean()=:0.2f}")

horizon = 30
A = RV({0: 1})  # Arrival time A_0
A += X  # Arrival time A_1
W = RV({0: 1})  # Waiting time W_1
# Mind that we start at 2 instead of 1
for i in range(2, horizon):
    A += X
    W = (W + S - X).map(Plus)

D = A + W + S # These are not the departure times!

print(f"{W.mean()=:0.2f}, {W.std()=:0.2f}")
print(f"{D.mean()=:0.2f}, {D.std()=:0.2f}")

num_runs = 1000
w30 = np.zeros(num_runs)
d30 = np.zeros(num_runs)
rng = np.random.default_rng(3)
for run_no in range(num_runs):
    x = X.rvs(horizon, rng)
    s = S.rvs(horizon, rng)
    x[0] = s[0] = w = 0
    for i in range(1, horizon):
        w = Plus(w + s[i - 1] - x[i])

    w30[run_no] = w
    a = x.cumsum()
    d30[run_no] = a[i] + w + s[i]

print(f"{w30.mean()=:0.2f}, {w30.std()=:0.2f}")
print(f"{d30.mean()=:0.2f}, {d30.std()=:0.2f}")

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(6, 3))
ax1.set_title("Waiting times cdf")
ax1.set_xlabel("Time")
ax1.plot(
    W.support(), [W.cdf(k) for k in W.support()], c='k', lw=0.75, label="exact"
)
ax1.hist(
    w30,
    bins=30,
    density=True,
    cumulative=True,
    histtype='step',
    align="right",
    color='k',
    lw=0.5,
    label="sim",
)
ax1.legend()

ax2.set_title("Waiting times pmf")
ax2.set_xlabel("Time")
ax2.hist(
    w30,
    bins=30,
    density=True,
    histtype='step',
    align="right",
    color='k',
    lw=0.7,
    label="sim",
)
x = W.support()
y = [W.pmf(k) for k in W.support()]
ax2.plot(x, y, color='k', lw=0.75, label="exact")
ax2.legend()
fig.tight_layout()
fig.savefig("../figures/waiting_time_distribution.pdf")

X = RV({4.1: 1 / 3, 5: 1 / 3, 3: 1 / 3})
S = RV({4: 1 / 3, 5: 1 / 3, 7: 1 / 3})

horizon = 30
A = RV({0: 1})  # arrival time
W = RV({0: 1})  # waiting time
for i in range(1, horizon):
    A += X
    W = (W + S - X).map(Plus)

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(6, 3))
ax1.set_title("Waiting times cdf")
ax1.set_xlabel("Time")
ax1.plot(
    W.support(), [W.cdf(k) for k in W.support()], c='k', lw=0.75, label="exact"
)
ax2.set_title("Waiting times pmf")
ax2.set_xlabel("Time")
ax2.plot(
    W.support(), [W.pmf(k) for k in W.support()], c='k', lw=0.75, label="exact"
)

fig.tight_layout()
fig.savefig("../figures/waiting_time_distribution_pmf_4.1.pdf")
