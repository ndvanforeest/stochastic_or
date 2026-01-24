from functools import cache

from random_variable import NumericRV as RV
from functions import Plus, Min

from lighthouse_case import D, K, N, l, h, b


class Qr:
    def __init__(self, D, l, h, b):
        self.D = D
        self.l = l
        self.h = h
        self.b = b
        self.X = sum(self.D for _ in range(l)) if l > 0 else RV({0: 1})

    @cache
    def IP(self, Q, r):
        return RV({i: 1 / Q for i in range(r + 1, r + Q + 1)})

    @cache
    def IL(self, Q, r):
        return self.IP(Q, r) - self.X

    @cache
    def Imin(self, Q, r):
        return self.IL(Q, r).map(lambda x: Min(x))

    @cache
    def Iplus(self, Q, r):
        return self.IL(Q, r).map(lambda x: Plus(x))

    def cost(self, Q, r):
        return (
            self.b * self.Imin(Q, r).mean() + self.h * self.Iplus(Q, r).mean()
        )

    def alpha(self, Q, r):
        return (self.IL(Q, r) - self.D).sf(-1)

    def beta(self, Q, r):
        m = RV.map2(self.D, self.Iplus(Q, r), lambda x, y: min(x, y))
        return m.mean() / self.D.mean()


qr = Qr(D, l, h, b)
Q, r = 3, 10
print(qr.IL(Q, r).mean())
print((Q + 1) / 2 + r - qr.X.mean())
