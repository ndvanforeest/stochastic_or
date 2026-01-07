from random_variable import RV

labda_B, mu = 1, 3
B = RV({1: 1, 2: 1, 3: 1})
rho = labda_B * B.mean() / mu
rho_B = labda_B / mu


def mxm1(eps=1e-10):
    "Compute stationary distribution of number of job in the system."
    "We the probabilities decrease geometrically fast."
    if rho >= 1:
        print("The load is too high")
        quit()
    pi, n = [1], 0
    batch_sizes = [int(m) - 1 for m in B.support()]
    while n < batch_sizes[-1]:
        res = sum(pi[m] * B.sf(n - m) for m in range(n + 1))
        pi.append(res * rho_B)
        n += 1
    while pi[-1] > eps:
        res = sum(pi[n - m] * B.sf(m) for m in batch_sizes)
        pi.append(res * rho_B)
        n += 1
    return RV({i: pi[i] for i in range(len(pi))})


def complete_rejection(K):
    pi, n = {}, 0
    pi[0] = 1
    while n < K:
        pi[n + 1] = sum(
            pi[m] * (B.sf(n - m) - B.sf(K - m)) for m in range(n + 1)
        )
        pi[n + 1] *= rho_B
        n += 1
    return RV(pi)


def partial_acceptance(K):
    pi, n = {}, 0
    pi[0] = 1
    while n < K:
        pi[n + 1] = sum(pi[m] * B.sf(n - m) for m in range(n + 1))
        pi[n + 1] *= rho_B
        n += 1
    return RV(pi)


def complete_acceptance(K):
    pi, n = {}, 0
    pi[0] = 1
    while B.sf(n - K) > 0:
        pi[n + 1] = sum(pi[m] * B.sf(n - m) for m in range(min(n, K) + 1))
        pi[n + 1] *= rho_B
        n += 1
    return RV(pi)


pi = mxm1()
print(pi.mean())

pi = complete_rejection(5)
print(pi.mean())
pi = partial_acceptance(5)
print(pi.mean())
pi = complete_acceptance(5)
print(pi.mean())
