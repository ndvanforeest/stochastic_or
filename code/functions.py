import numpy as np


def normalize(pmf):
    norm = sum(pmf.values())
    return {k: pk / norm for k, pk in pmf.items()}


def grid_search(grid, f):
    "Minimize a f on the grid."
    best_x, best_value = None, float('inf')
    for x in grid:
        if not isinstance(x, (tuple, list)):
            x = (x,)
        value = f(*x)
        if value < best_value:
            best_x, best_value = x, value
    return best_x, best_value


def Plus(x):
    if isinstance(x, (int, float)):
        return max(x, 0)
    elif isinstance(x, (list, tuple)):
        return [Plus(v) for v in x]
    else:
        return np.maximum(x, 0)


def Min(x):
    if isinstance(x, (int, float)):
        return Plus(-x)
    elif isinstance(x, (list, tuple)):
        return [Min(v) for v in x]
    else:
        return Plus(-x)
