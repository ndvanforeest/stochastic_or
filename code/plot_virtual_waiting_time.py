"""Generate the figure for the simulation of continuous time queueing processes."""

import heapq

import matplotlib.pyplot as plt
import numpy as np

from latex_figures import apply_figure_settings

apply_figure_settings(use=True)

rng = np.random.default_rng(3)
labda, mu = 3, 4
num = 10
X = rng.exponential(scale=1 / labda, size=num)
S = rng.exponential(scale=1 / mu, size=num)
X[0] = S[0] = 0
D = np.zeros_like(X)

A = X.cumsum()
for i in range(1, num):
    D[i] = max(A[i], D[i - 1]) + S[i]

J = D - A
W = J - S

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(6, 3), sharex=True)
ax1.set_ylabel("Work $W$")
ax2.set_ylabel("Length $L$")
ax2.set_xlabel("time")
ax2.set_yticks([0, 1, 2, 3, 4, 5])

for i in range(1, num):
    ax1.fill([A[i], A[i], D[i]], [0, J[i], 0], c='green', alpha=0.2)
    ax1.fill([A[i], A[i], A[i] + W[i]], [0, W[i], 0], c='blue', alpha=0.2)

def At(t, side='right'):
    "The right or left continuous version of A(t)."
    return max(np.searchsorted(A, t, side=side) - 1, 0)

def W(t, side='right'):
    "The right or left continuous work in the system."
    k = At(t, side)
    return max(D[k] - t, 0)

arrivals = [(t, 1) for t in A[1:]]
departures = [(t, -1) for t in D[1:]]
events = list(heapq.merge(arrivals, departures))
heapq.heapify(events)

L, past = 0, 0
while events:
    now, delta = heapq.heappop(events)
    ax1.plot([past, now], [W(past), W(now, 'left')], c='k', lw=0.75)
    ax1.plot([now, now], [W(now, 'left'), W(now)], ":", c='k', lw=0.75)
    ax2.plot([past, now], [L, L], c='k', lw=0.75)
    ax2.plot([now, now], [L, L + delta], ":", c='k', lw=0.75)
    L += delta
    past = now

fig.tight_layout()
fig.savefig('../figures/queue-continuous-length.pdf')
fig.savefig('../figures/queue-continuous-length.png', dpi=300)
