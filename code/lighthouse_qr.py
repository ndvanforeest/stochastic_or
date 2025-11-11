from functools import cache
import numpy as np

import random_variable as rv


class Qr:
    def __init__(self, D, L, h, b):
        self.D = D
        self.L = L
        self.h = h
        self.b = b
        self.X = sum(self.D for i in range(self.L))

    @cache
    def IP(self, Q, r):
        return rv.RV({i: 1 / Q for i in range(r + 1, r + Q + 1)})

    @cache
    def IL(self, Q, r):
        return self.IP(Q, r) - self.X

    @cache
    def Imin(self, Q, r):
        return rv.apply_function(lambda x: max(0, -x), self.IL(Q, r))

    @cache
    def Iplus(self, Q, r):
        return rv.apply_function(lambda x: max(0, x), self.IL(Q, r))

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
L = 2
c = 100  # buying price
b = 0.1 * c  # backlog
h = 0.5 * c / 30  # holding
S = 5


qr = Qr(D, L, h, b)
Q, r = 3, 10
print(qr.IL(Q, r).mean())
print((Q + 1) / 2 + r - qr.X.mean())
