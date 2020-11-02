#!/usr/bin/env python3
# cronbachs-alpha-nodep.py

#%% import-libraries
from math import isnan
from statistics import variance
from typing import List

#%% define-function
def cronbach_alpha(rows: List[list]) -> float:
    """
    Calculate Cronbach's alpha.

    Parameters
    ----------
    rows : List[list]
        A table (list of lists) of numeric values. Each inner list 
        represents a row.

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
    cols = [*zip(*rows)]
    
    colvars = [variance(x for x in col if not isnan(x)) for col in cols]
    rowsums = [sum(x for x in row if not isnan(x)) for row in rows]
    
    k = len(cols)
    sum_of_variances = sum(colvars)
    variance_of_sums = variance(rowsums)
    
    alpha = k / (k - 1) * (1 - (sum_of_variances / variance_of_sums))
    
    return alpha

#%% main
def main():
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()
