from abc import ABC, abstractmethod
from functools import cache

import numpy as np
from functions import Min, Plus
from random_variable import NumericRV as RV


class InventoryModelPrimitives:
    "Common functionality for sS and TsS inventory control systems."

    def __init__(self, D, leadtime, h, b, K):
        if D.pmf(0) == 1:
            raise ValueError("Invalid D: pmf(0) == 1")
        self.D = D
        self.leadtime = leadtime
        self.h = h
        self.b = b
        self.K = K
        self.X = sum(self.D for _ in range(leadtime)) if leadtime > 0 else RV({0: 1})

    def c(self, x):
        return self.b * Min(x) + self.h * Plus(x)

    @cache
    def L(self, x):
        return self.X.E(lambda i: self.c(x - i))

    @abstractmethod
    def hitting_value(self, *, running_cost, stopping_cost):
        raise NotImplementedError

    @cache
    def hitting_cost(self, *args, **kwargs):
        return self.hitting_value(
            running_cost=lambda x: self.L(x),
            stopping_cost=lambda x: self.K,
        )(*args, **kwargs)

    @cache
    def hitting_time(self, *args, **kwargs):
        return self.hitting_value(
            running_cost=lambda x: 1.0,
            stopping_cost=lambda x: 0.0,
        )(*args, **kwargs)

    def average_cost(self, *args, **kwargs):
        return self.hitting_cost(*args, **kwargs) / self.hitting_time(
            *args, **kwargs
        )
