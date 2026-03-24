from functools import cache

from inventory_base import InventoryModelPrimitives


class TsSPolicy(InventoryModelPrimitives):
    def hitting_value(self, *, running_cost, stopping_cost):
        is_stop = lambda n, s, x: x <= s or n == 0

        @cache
        def v(T, s, S):
            if is_stop(T, s, S):
                return stopping_cost(S)
            return running_cost(S) + self.D.E(lambda i: v(T - 1, s, S - i))

        return v


class TSPolicy(TsSPolicy):
    "Long run average cost for a TS inventory system."

    def average_cost(self, T, S):
        return super().average_cost(T, -float('inf'), S)
