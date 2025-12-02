"""Lighthouse case: model parameters."""
import random_variable as rv

D = rv.RV({0: 1 / 6, 1: 1 / 5, 2: 1 / 4, 3: 1 / 8, 4: 11 / 120, 5: 1 / 6})

l = 2  # lead time
h = 40 * 0.5 / 30  # daily holding cost
b = 100 * 0.2  # daily backlog cost
K = 50  # Order cost, used for sS and Qr
N = 100  # simulation duration

if N <= l:
    print(f"The simulation duration {N=} is shorter than the leadtime {l=}.")
    quit()
