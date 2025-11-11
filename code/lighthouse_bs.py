from functools import cache
import numpy as np

import random_variable as rv

class Basestock:
    """Implements KPIs for a basestock inventory system."""

    def __init__(self, D, L, h, b):
        self.D = D
        self.L = L
        self.h = h
        self.b = b
        self.X = sum(self.D for _ in range(self.L))

    @cache
    def IP(self, S):
        return S

    @cache
    def IL(self, S):
        return self.IP(S) - self.X

    @cache
    def Imin(self, S):
        return rv.apply_function(lambda x: max(0, -x), self.IL(S))

    @cache
    def Iplus(self, S):
        return rv.apply_function(lambda x: max(0, x), self.IL(S))

    def cost(self, S):
        return self.b * self.Imin(S).mean() + self.h * self.Iplus(S).mean()

    def alpha(self, S):
        return (self.IL(S) - self.D).sf(-1)

    def beta(self, S):
        m = rv.compose_function(lambda x, y: min(x, y), self.D, self.Iplus(S))
        return m.mean() / self.D.mean()

D = rv.RV({0: 1 / 6, 1: 1 / 5, 2: 1 / 4, 3: 1 / 8, 4: 11 / 120, 5: 1 / 6})
L = 2
c = 100  # buying price
b = 0.1 * c  # backlog
h = 0.5 * c / 30  # holding
S = 5

base = Basestock(D, L, h, b)

theta = L * D.mean()
print(np.isclose(base.IL(S).mean(), S - theta))
print(np.isclose(
    base.Imin(S).mean(), theta - sum(base.X.sf(j) for j in range(0, S))
))
print(np.isclose(base.alpha(S), (base.X + D).cdf(S)))

for S in range(5, 11):
    print(f"{S=}: {base.alpha(S)=:.2f}, {base.beta(S)=:.2f}, {base.cost(S)=:.2f}")
