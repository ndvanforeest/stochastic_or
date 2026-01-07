from functools import cache
import numpy as np

import random_variable as rv
from functions import Plus, Min

from lighthouse_case import D, l, h, b

class Basestock:
    """Implements KPIs for a basestock inventory system."""

    def __init__(self, D, l, h, b):
        self.D = D
        self.l = l
        self.h = h
        self.b = b
        self.X = sum(self.D for _ in range(l)) if l > 0 else rv.RV({0: 1})

    @cache
    def IP(self, S):
        return S

    @cache
    def IL(self, S):
        return self.IP(S) - self.X

    @cache
    def Imin(self, S):
        return rv.apply_function(lambda x: Min(x), self.IL(S))

    @cache
    def Iplus(self, S):
        return rv.apply_function(lambda x: Plus(x), self.IL(S))

    def cost(self, S):
        return self.b * self.Imin(S).mean() + self.h * self.Iplus(S).mean()

    def alpha(self, S):
        return (self.IL(S) - self.D).sf(-1)

    def beta(self, S):
        m = rv.compose_function(lambda x, y: min(x, y), self.D, self.Iplus(S))
        return m.mean() / self.D.mean()

S = 5

base = Basestock(D, l, h, b)

theta = l * D.mean()
print(np.isclose(base.IL(S).mean(), S - theta))
print(
    np.isclose(
        base.Imin(S).mean(), theta - sum(base.X.sf(j) for j in range(0, S))
    )
)
print(np.isclose(base.alpha(S), (base.X + D).cdf(S)))

for S in range(5, 12):
    print(f"{S=}: {base.alpha(S)=:.2f}, {base.beta(S)=:.2f}, {base.cost(S)=:.2f}")
