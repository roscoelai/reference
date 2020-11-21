#!/usr/bin/env python3
# cronbachs-alpha-mindep.py

#%% import-libraries
import numpy as np
from time import perf_counter

#%% define-functions
def cronbach_alpha(X: np.ndarray) -> float:
    """
    Calculate Cronbach's alpha.

    :param X: a matrix of numerical values
    :returns: Cronbach's alpha
    :raises TypeError: if X is not all numeric

    >>> cronbach_alpha(np.array([[1, 1], [2, 2]]))
    1.0

    >>> cronbach_alpha(np.array([[1, 1], [1, 2]]))
    0.0

    >>> np.random.seed(123); cronbach_alpha(np.random.randint(0, 5, (30, 5)))
    0.1763577331759146
    """
    A = np.array(X)
    k = A.shape[1]
    colvars = np.nanvar(A, axis=0, ddof=1)
    rowsums = np.nansum(A, axis=1)
    return (1 - (np.sum(colvars) / np.var(rowsums, ddof=1))) * k / (k - 1)

#%% main
def main():
    import doctest
    t1 = perf_counter()
    doctest.testmod(verbose=True)
    t2 = perf_counter()
    print("Time taken: {:.6f} sec".format(t2 - t1))

if __name__ == "__main__":
    main()
