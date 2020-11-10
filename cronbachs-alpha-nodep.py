#!/usr/bin/env python3
# cronbachs-alpha-nodep.py

#%% import-libraries
from itertools import filterfalse
from math import isnan
from statistics import variance
from time import perf_counter
from typing import List, Union

#%% define-functions
Number = Union[int, float]

def cronbach_alpha(rows: List[List[Number]]) -> float:
    """
    Calculate Cronbach's alpha.

    Parameters
    ----------
    rows : List[List[Number]]
        A list of lists. Each inner list represents a row in a table.

    Returns
    -------
    float
        Cronbach's alpha.

    >>> cronbach_alpha([[1, 1], [2, 2]])
    1.0

    >>> cronbach_alpha([[1, 1], [1, 2]])
    0.0
    
    >>> round(cronbach_alpha([[1, 1], [1, float("nan")], [1, 3]]), 6)
    0.285714
    """
    k = len(rows[0])
    colvars = (variance(filterfalse(isnan, col)) for col in zip(*rows))
    rowsums = (sum(filterfalse(isnan, row)) for row in rows)
    return (1 - (sum(colvars) / variance(rowsums))) * k / (k - 1)

#%% main
def main():
    import doctest
    t1 = perf_counter()
    doctest.testmod(verbose=True)
    t2 = perf_counter()
    print("Time taken: {:.6f} sec".format(t2 - t1))

if __name__ == "__main__":
    main()
