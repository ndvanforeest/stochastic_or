import numpy as np
from numpy.random import default_rng

import random_variable as rv

demand = rv.RV({0: 1 / 6, 1: 1 / 5, 2: 1 / 4, 3: 1 / 8, 4: 11 / 120, 5: 1 / 6})

l = 2  # lead time
h = 40 * 0.5 / 30  # daily holding cost
b = 100 * 0.2  # daily backlog cost
K = 50
N = 100  # simulation duration

if N <= l:
    print(f"The simulation duration {N=} is shorter than the leadtime {l=}.")
    quit()

def simulate_sS(D, s, S):
    P = np.zeros(N)  # inventory position
    Q = np.zeros(N)  # order quantities
    IL = np.zeros(N)  # inventory level
    P[0] = IL[0] = S  # initial values

    for t in range(1, N):
        Pprime = P[t - 1] - D[t - 1]
        Q[t] = (S - Pprime) * (Pprime <= s)
        P[t] = Pprime + Q[t]

    for t in range(1, N):
        IL[t] = IL[t - 1] - D[t - 1]
    for t in range(min(l, N), N):
        IL[t] = IL[t - 1] - D[t - 1] + Q[t - l]

    return P, IL, Q

def Iplus(IL):
    return np.maximum(IL, 0)


def Imin(IL):
    return np.maximum(-IL, 0)


def cost(IL, Q):
    return K * (Q > 0).mean() + h * Iplus(IL).mean() + b * Imin(IL).mean()


def alpha(IL):
    return (IL >= 0).mean()


def beta(D, IL):
    return np.minimum(D, Iplus(IL)).sum() / D.sum()


def alpha_c(IL, Q):
    return ((Q[:-l] > 0) * (IL[l - 1 : -1] >= 0)).sum() / (Q[:-l] > 0).sum()

rng = default_rng(3)  # set the seed
D = demand.rvs(size=N, random_state=rng)

P, IL, Q = simulate_sS(D, s=3, S=20)

print(f"{D.mean()=:.2f}, {P.mean()=:.2f}, {IL.mean()=:.2f}, {Q.mean()=:.2f}")
print(f"{Iplus(IL).mean()=:.2f}, {Imin(IL).mean()=:.2f}")
print(f"{cost(IL, Q)=:.2f}")
print(f"{alpha(IL)=:.2f}, {beta(D, IL)=:.2f}, {alpha_c(IL, Q)=:.2f}")

min_cost, s_opt, S_opt = np.inf, 0, 0
for s in range(-5, 10):
    for S in range(s + 1, 50):
        P, IL, Q = simulate_sS(D, s=s, S=S)
        C = cost(IL, Q)
        if C < min_cost:
            min_cost, s_opt, S_opt = C, s, S

print(f"{s_opt=}, {S_opt=}, {min_cost=:.2f}")
