from functools import cache

from inventory_base import InventoryModelPrimitives


class sSPolicy(InventoryModelPrimitives):
    def hitting_value(self, *, running_cost, stopping_cost):
        is_stop = lambda s, x: x <= s

        @cache
        def v(s, S):
            if is_stop(s, S):
                return stopping_cost(S)
            res = running_cost(S)
            res += self.D.E(lambda i: 0.0 if i == 0 else v(s, S - i))
            return res / (1.0 - self.D.pmf(0))

        return v
