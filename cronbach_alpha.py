#!/usr/bin/env -S conda run -n env1 python
# File: cronbach_alpha.py

import numpy as np

def cronbach_alpha(A: np.ndarray) -> float:
    """Return Cronbach's alpha for the given input array.

    A : Matrix of numerical values for the relevant columns/features

    >>> cronbach_alpha(np.array([[1, 1], [2, 2]]))
    1.0
    >>> cronbach_alpha(np.array([[1, 1], [1, 2]]))
    0.0
    >>> np.random.seed(123); cronbach_alpha(np.random.randint(0, 5, (30, 5)))
    0.1763577331759146
    """
    A = np.array(A)
    k = A.shape[1]
    item_vars = np.nanvar(A, axis=0, ddof=1)
    sum_items = np.nansum(A, axis=1)
    ratio = np.sum(item_vars) / np.var(sum_items, ddof=1)
    return k / (k - 1) * (1 - ratio)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
