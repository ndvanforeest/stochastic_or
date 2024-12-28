"""
The class RV enables probabilistic arithmetic, such as addition or
 division, with independent discrete random variables.

The comments starting with the code word "block" have an
educational purpose. In an org mode file I import specific lines of the
RV class, and the block comments are used to compute the compute the
correct line number to include.
"""

# block modules
import operator
from collections import defaultdict
from fractions import Fraction
from functools import cache
from typing import Callable, Union

import numpy as np
from numpy.random import default_rng

numeric = Union[int, Fraction, float]
# block modules


# block numbers
max_denominator = 1_000_000
thres = 1e-16  # Reject probabilities smaller than this.
seed = 3  # For the random number generator.


def toFrac(x: float | int | Fraction):
    "Convert x to fraction of specified precision."
    return Fraction(x).limit_denominator(max_denominator)


# block numbers


# block startofrv
class RV:
    "A random variable whose  keys for the support and values the pmfs."

    def __init__(self, pmf: dict[numeric, float]):
        self._pmf = self.make_pmf(pmf)
        self._support = np.array(sorted(self._pmf.keys()))
        self._cdf = np.cumsum([self._pmf[k] for k in self._support])

    # block startofrv

    # block makepmf
    def make_pmf(self, pmf):
        res: dict[Fraction, float] = defaultdict(float)
        for k, pk in pmf.items():
            res[toFrac(k)] += pk if pk >= thres else 0
        res = {k: v for k, v in res.items() if v > 0}  # no prob zero events.
        return self.normalize(res)

    def normalize(self, pmf):
        norm = sum(pmf.values())
        return {k: pk / norm for k, pk in pmf.items()}

    # block makepmf

    # block pmf
    def pmf(self, x: numeric) -> float:
        return self._pmf.get(toFrac(x), 0)

    def support(self) -> np.ndarray:
        return self._support

    def __len__(self):
        return len(self._support)

    def __repr__(self):
        return "".join(f"{k}: {self._pmf[k]}, " for k in self._support)

    # block pmf

    # block support
    @cache
    def sortedsupport(self) -> np.array:
        "Return the support sorted in decreasing order of the pmf."
        return np.array(sorted(self._pmf, key=self._pmf.get, reverse=True))

    # block support

    # block cdf
    @cache
    def cdf(self, x: numeric) -> float:
        if x < self._support[0]:
            return 0
        if x >= self._support[-1]:
            return 1
        return self._cdf[np.searchsorted(self._support, x)]

    def sf(self, x: float) -> float:
        "Survivor function"
        return 1 - self.cdf(x)

    # block cdf

    # block expected
    def E(self, f: Callable[[numeric], numeric]) -> float:
        "Compute E(f(X))"
        return sum(f(i) * self.pmf(i) for i in self.support())

    # block expected

    # block convenience
    @cache
    def mean(self) -> float:
        return self.E(lambda x: x)

    @cache
    def var(self) -> float:
        return self.E(lambda x: x**2) - self.mean() ** 2

    @cache
    def sdv(self) -> float:
        return np.sqrt(self.var())

    # block convenience

    # block rvs
    def rvs(self, size: int = 1, random_state=default_rng(seed)) -> np.ndarray:
        "Generate an array with 'size' number of random deviates."
        U: np.ndarray = random_state.uniform(size=size)
        pos: np.ndarray = np.searchsorted(self._cdf, U)
        return self.support()[pos].astype(float)

    # block rvs

    # block arithmetic

    def __add__(self, other: 'RV') -> 'RV':
        other = convert(other)
        return compose_function(operator.add, self, other)

    def __neg__(self):
        return RV({-k: self.pmf(k) for k in self.support()})

    def __sub__(self, other: 'RV') -> 'RV':
        return self + (-other)

    def __truediv__(self, other: 'RV') -> 'RV':
        other = convert(other)
        return compose_function(operator.truediv, self, other)

    def __mul__(self, other: 'RV') -> 'RV':
        other = convert(other)
        return compose_function(operator.mul, self, other)

    # block arithmetic

    # block sums
    def __radd__(self, other):
        # support sum([rv for i in ...])
        return self.__add__(convert(other))

    def __rsub__(self, other: 'RV') -> 'RV':
        return convert(other).__sub__(self)  # mind the sequence of b - a

    # block sums

    # block equality
    def __eq__(self, other):
        return self._pmf == other._pmf

    def __hash__(self):
        return id(self)

    # block equality


# block compose
def compose_function(
    f: Callable[[numeric, numeric], float], X: RV, Y: RV
) -> RV:
    "Make the rv f(X, Y) for the independent rvs X and Y."
    c: defaultdict[Fraction, float] = defaultdict(float)
    for i in X.sortedsupport():
        for j in Y.sortedsupport():
            p = X.pmf(i) * Y.pmf(j)
            c[f(i, j)] += p
            if p <= thres:
                break
    return RV(c)


# block compose


# block apply
def apply_function(f: Callable[[numeric], numeric], X: RV) -> RV:
    "Make the rv f(X)"
    c: defaultdict[Fraction, float] = defaultdict(float)
    for k in X.support():
        c[f(k)] += X.pmf(k)
    return RV(c)


# block apply


# block convert
def convert(rv):
    "Check and convert to rv if necessary."
    match rv:
        case RV():
            return rv
        case int():
            return RV({rv: 1})  # An int is a shift.
        case float():
            return RV({rv: 1})  # A float is a shift too.
        case _:
            raise ValueError("Unknown type passed as a RV")


# block convert


# block tests
def tests():
    U = RV({1: 1})
    V = RV({2: 1})
    X = RV({1: 1 / 3, 2: 2 / 3})
    Y = RV({-1: 1 / 3, -2: 2 / 3})

    assert np.all((U + X).support() == np.array([2, 3]))
    assert -X == Y
    assert (U + V).pmf(2) == 0
    assert (U + V).pmf(3) == 1
    assert np.isclose(U.var(), 0)
    assert np.isclose(X.pmf(0.99999999999), 1 / 3)
    assert np.isclose(X.mean(), 1 / 3 + 2 * 2 / 3)
    assert np.isclose(X.sf(1), 2 / 3)


# block tests


def main():
    tests()


if __name__ == '__main__':
    main()
