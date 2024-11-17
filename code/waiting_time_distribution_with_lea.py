import numpy as np
import lea
from icecream import ic
import random_variable as rv


def Plus(x):
    return max(x, 0)


horizon = 5

x_dict = {4: 1 / 3, 5: 1 / 3, 3: 1 / 3}  # inter arrival times
s_dict = {4: 1 / 3, 5: 1 / 3, 7: 1 / 3}  # service times


X = lea.pmf(x_dict)
S = lea.pmf(s_dict)
null = lea.pmf({0: 1})

A = null.new()  # arrival time
D = null.new()  # departure time
for i in range(1, horizon):
    A += X.new()
    D = lea.max_of(A, D) + S.new()
    # D = lea.max_of(A.new(), D.new()) + S.new()

W = null.new()
# Observe that the first job that arrives does not have to wait.
# hence the start at 2 instead of 1
for i in range(2, horizon):
    W = lea.max_of(W + S.new() - X.new(), null, fast=True)
    # W = lea.max_of(W + S.new() - X.new(), null)

D_W = A + W + S.new()

ic(D_W.mean, D.mean)
ic(D_W.var, D.var)

X = rv.RV(x_dict)
S = rv.RV(s_dict)


A = rv.RV({0: 1})  # arrival time
W = rv.RV({0: 1})  # waiting time
A += X
# W1 = 0, arrives at empty system
for i in range(2, horizon):
    A += X
    W = rv.apply_function(Plus, W + S - X)

D = A + W + S
ic(D_W.mean, D.mean())
ic(D_W.var, D.var())

num_sim = 10000
D_sim = np.zeros(num_sim)
DW_sim = np.zeros(num_sim)
W_sim = np.zeros(num_sim)
for n in range(num_sim):
    x = X.rvs(horizon)
    s = S.rvs(horizon)
    x[0] = s[0] = 0
    a = d = w = 0
    for i in range(1, horizon):
        a += x[i]
        d = max(a, d) + s[i]
        w = max(w + s[i - 1] - x[i], 0)
    D_sim[n] = d
    DW_sim[n] = a + w + s[i]
    W_sim[n] = w


ic(W_sim.mean(), W.mean())
ic(W_sim.var(), W.var())
ic(D_sim.mean(), D.mean())
ic(D_sim.var(), D.var())
ic(DW_sim.mean(), D.mean())
ic(DW_sim.var(), D.var())

# ic(D_sim.mean(), D.mean, D_W.mean, D_n.mean())
# ic(D_sim.var(), D.var, D_W.var, D_n.var())
# ic(W_sim.mean(), W_lea.mean, W_n.mean())
# ic(W_lea.var, W_sim.var(), W_n.var())

# quit()
# fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(6, 3))
# ax1.plot(D.support, D.ps, lw=1, label="D")
# ax1.plot(D_W.support, D_W.ps, ":", c='blue', lw=0.75, label="D_wait")
# # ax1.plot(D_W.support, D_W.ps, ":", c='blue', lw=0.75, label="D_wait")
# ax1.legend()
# ax2.plot(W_lea.support, W_lea.ps, c="k", lw=3, label="W_lea")
# ax2.plot(W_fast.support, W_fast.ps, c='white', lw=0.75, label="W_fast")
# ax2.legend()


# fig.tight_layout()
# fig.savefig("lea.pdf")
