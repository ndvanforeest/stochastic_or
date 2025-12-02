import numpy as np
from numpy.random import default_rng

import random_variable as rv
from  functions import Plus, Min

from lighthouse_case import D, K, N, l, h, b

def simulate_sS(demands, s, S):
    P = np.zeros(N)  # inventory position
    Q = np.zeros(N)  # order quantities
    IL = np.zeros(N)  # inventory level
    P[0] = IL[0] = S  # initial values

    for t in range(1, N):
        Pprime = P[t - 1] - demands[t - 1]
        Q[t] = (S - Pprime) * (Pprime <= s)
        P[t] = Pprime + Q[t]

    for t in range(1, N):
        IL[t] = IL[t - 1] - demands[t - 1]
    for t in range(min(l, N), N):
        IL[t] = IL[t - 1] - demands[t - 1] + Q[t - l]

    return P, IL, Q

def cost(IL, Q):
    return K * (Q > 0).mean() + h * Plus(IL).mean() + b * Min(IL).mean()


def alpha(IL):
    return (IL >= 0).mean()


def beta(demands, IL):
    return np.minimum(demands, Plus(IL)).sum() / demands.sum()


def alpha_c(IL, Q):
    return ((Q[:-l] > 0) * (IL[l - 1 : -1] >= 0)).sum() / (Q[:-l] > 0).sum()

rng = default_rng(3)  # set the seed
demands = D.rvs(size=N, random_state=rng)

P, IL, Q = simulate_sS(demands, s=3, S=20)

print(f"{demands.mean()=:.2f}, {P.mean()=:.2f}, {IL.mean()=:.2f}, {Q.mean()=:.2f}")
print(f"{Plus(IL).mean()=:.2f}, {Min(IL).mean()=:.2f}")
print(f"{cost(IL, Q)=:.2f}")
print(f"{alpha(IL)=:.2f}, {beta(demands, IL)=:.2f}, {alpha_c(IL, Q)=:.2f}")

def cost_of(demands, s, S):
    P, IL, Q = simulate_sS(demands, s, S)
    return cost(IL, Q)

from functions import grid_search

pairs = ((s, S) for s in range(-5, 10) for S in range(s + 1, 30))
(s_opt, S_opt), V = grid_search(pairs, lambda s, S: cost_of(demands, s, S))

print(f"{s_opt=}, {S_opt=}, {V=:.2f}")
