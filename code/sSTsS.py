from abc import ABC, abstractmethod
from functools import cache

import numpy as np
from functions import Min, Plus
from random_variable import NumericRV as RV


class InventoryModelPrimitives:
    "Common functionality for sS and TsS inventory control systems."

    def __init__(self, D, l, h, b, K):
        if D.pmf(0) == 1:
            raise ValueError("Invalid D: pmf(0) == 1")
        self.D = D
        self.D = D
        self.l = l
        self.h = h
        self.b = b
        self.K = K
        self.X = sum(self.D for _ in range(l)) if l > 0 else RV({0: 1})

    def c(self, x):
        return self.b * Min(x) + self.h * Plus(x)

    @cache
    def L(self, x):
        return self.X.E(lambda i: self.c(x - i))

    @abstractmethod
    def hitting_value(self, *, running_cost, terminal_cost):
        raise NotImplementedError

    @cache
    def hitting_cost(self, *args, **kwargs):
        return self.hitting_value(
            running_cost=lambda x: self.L(x),
            terminal_cost=lambda x: self.K,
        )(*args, **kwargs)

    @cache
    def hitting_time(self, *args, **kwargs):
        return self.hitting_value(
            running_cost=lambda x: 1.0,
            terminal_cost=lambda x: 0.0,
        )(*args, **kwargs)

    def average_cost(self, *args, **kwargs):
        return self.hitting_cost(*args, **kwargs) / self.hitting_time(
            *args, **kwargs
        )

class TsSPolicy(InventoryModelPrimitives):
    def hitting_value(self, *, running_cost, terminal_cost):
        stop = lambda n, s, x: x <= s or n == 0

        @cache
        def v(T, s, S):
            if stop(T, s, S):
                return terminal_cost(S)
            return running_cost(S) + self.D.E(lambda i: v(T - 1, s, S - i))

        return v

class sSPolicy(InventoryModelPrimitives):
    def hitting_value(self, *, running_cost, terminal_cost):
        stop = lambda s, x: x <= s

        @cache
        def v(s, S):
            if stop(s, S):
                return terminal_cost(S)
            res = running_cost(S)
            res += self.D.E(lambda i: 0.0 if i == 0 else v(s, S - i))
            return res / (1.0 - self.D.pmf(0))

        return v

class TSPolicy(TsSPolicy):
    "Long run average cost for a TS inventory system."

    def average_cost(self, T, S):
        return super().average_cost(T, -np.inf, S)

class BasestockPolicy(sSPolicy):
    "Implements KPIs for a basestock inventory system."

    def __init__(self, D, l, h, b):
        super().__init__(D, l, h, b, K=0)

    def average_cost(self, S):
        return super().average_cost(S - 1, S)
