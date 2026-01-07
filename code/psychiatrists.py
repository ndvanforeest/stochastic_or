# block modules
import numpy as np
from numpy.random import default_rng

# from fig_in_latex_format import apply_figure_settings

# apply_figure_settings()


thres_low = 24
thres_high = 48

# block modules


# block simple queue
def compute_L(a, c, L0=0):
    # L0 is the initial queue length
    L = np.empty(len(a))
    L[0] = L0
    for k in range(1, len(a)):
        d = min(L[k - 1] + a[k], c[k])
        L[k] = L[k - 1] + a[k] - d
    return L


a = np.ones(5)
c = np.ones(len(a))
L = compute_L(a, c)
print(L)

quit()

# block simple queue


# block control
def compute_L_with_control(a, c, e, L0=0):
    L = np.empty(len(a))
    L[0] = L0
    for k in range(1, len(a)):
        if L[k - 1] <= thres_low:
            c[k] -= e
        elif L[k - 1] >= thres_high:
            c[k] += e
        L[k] = max(L[k - 1] + a[k] - c[k], 0)
    return L


# block control


# block unbalanced
def unbalanced_load(n):
    p = np.empty([5, n])
    p[0, :] = 1 * np.ones(n)
    p[1, :] = 1 * np.ones(n)
    p[2, :] = 1 * np.ones(n)
    p[3, :] = 3 * np.ones(n)
    p[4, :] = 9 * np.ones(n)
    return p


# block unbalanced


# block Balanced
def balanced_load(n):
    p = np.empty([5, n])
    p[0, :] = 2 * np.ones(n)
    p[1, :] = 2 * np.ones(n)
    p[2, :] = 3 * np.ones(n)
    p[3, :] = 4 * np.ones(n)
    p[4, :] = 4 * np.ones(n)
    return p


# block Balanced


# block spread
def spread_holidays(p):
    n_cols = p.shape[1]
    for j in range(n_cols):
        p[j % 5, j] = 0
    return p


# block spread


# block synchronized
def synchronized_holidays(p):
    n_cols = p.shape[1]
    for j in range(0, n_cols, 5):
        p[:, j] = 0
    return p


# block synchronized


# block start sim
rng = default_rng(3)
num_weeks = 1000
a = rng.poisson(11.8, num_weeks)
L = np.zeros((4, len(a)))
# block start sim

# block scenarios
p = balanced_load(len(a))
p = spread_holidays(p)
c = np.sum(p, axis=0)
L[0, :] = compute_L(a, c)

p = balanced_load(len(a))
p = synchronized_holidays(p)
c = np.sum(p, axis=0)
L[1, :] = compute_L(a, c)

p = unbalanced_load(len(a))
p = synchronized_holidays(p)
c = np.sum(p, axis=0)
L[2, :] = compute_L(a, c)

p = unbalanced_load(len(a))
p = spread_holidays(p)
c = np.sum(p, axis=0)
L[3, :] = compute_L(a, c)
# block scenarios


# block plusminus
c = 12 * np.ones_like(a)
LL = np.zeros((4, len(a)))
LL[0, :] = compute_L(a, c)
LL[1, :] = compute_L_with_control(a, c, 1)
LL[2, :] = compute_L_with_control(a, c, 2)
LL[3, :] = compute_L_with_control(a, c, 5)
# block plusminus


# block figures
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(6, 3), sharey=True)
ax1.set_title("No control on $L$")
ax1.set_ylabel("Queue length")
ax1.set_xlabel("Time (weeks)")

ax1.plot(L.min(axis=0), ":", label="min", color='k', lw=0.5)
ax1.plot(L.max(axis=0), "-", label="max", color="k", lw=0.5)
ax1.legend()

ax2.set_title("Control on $L$")
ax2.set_xlabel("Time (weeks)")
ax2.plot(LL[1], label="$e = 1$", color='green', lw=0.8)
ax2.plot(LL[2], label="$e = 2$", color='blue', lw=0.5)
ax2.plot(LL[3], label="$e = 5$", color='red', lw=0.5)
ax2.legend()

fig.tight_layout()
fig.savefig("../figures/psychiatrists.png", dpi=300)
# block figures
