from functools import cache
import numpy as np

import random_variable as rv
from functions import Plus, Min


class Qr:
    def __init__(self, D, l, h, b):
        self.D = D
        self.l = l
        self.h = h
        self.b = b
        self.X = sum(self.D for _ in range(l)) if l > 0 else rv.RV({0: 1})

    @cache
    def IP(self, Q, r):
        return rv.RV({i: 1 / Q for i in range(r + 1, r + Q + 1)})

    @cache
    def IL(self, Q, r):
        return self.IP(Q, r) - self.X

    @cache
    def Imin(self, Q, r):
        return rv.apply_function(lambda x: Min(x), self.IL(Q, r))

    @cache
    def Iplus(self, Q, r):
        return rv.apply_function(lambda x: Plus(x), self.IL(Q, r))

    def cost(self, Q, r):
        return (
            self.b * self.Imin(Q, r).mean() + self.h * self.Iplus(Q, r).mean()
        )

    def alpha(self, Q, r):
        return (self.IL(Q, r) - self.D).sf(-1)

    def beta(self, Q, r):
        m = rv.compose_function(
            lambda x, y: min(x, y), self.D, self.Iplus(Q, r)
        )
        return m.mean() / self.D.mean()

D = rv.RV({0: 1 / 6, 1: 1 / 5, 2: 1 / 4, 3: 1 / 8, 4: 11 / 120, 5: 1 / 6})
l = 2
c = 100  # buying price
b = 0.1 * c  # backlog cost
h = 0.5 * c / 30  # holding cost

qr = Qr(D, l, h, b)
Q, r = 3, 10
print(qr.IL(Q, r).mean())
print((Q + 1) / 2 + r - qr.X.mean())
