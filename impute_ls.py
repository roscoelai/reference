#!/usr/bin/env -S conda run -n env1 python
# File: impute_ls.py

import numpy as np
from typing import Union

def impute_ls(A: np.ndarray, thresh: Union[int, float]=None, rounding=False):
    """Impute blanks in an array

    Returns the given array with blanks filled in using least-squares 
    imputation. Only the rows with number of blanks <= thresh would be 
    imputed. If there are no valid cases for imputation, return the original 
    array.

    >>> print(impute_ls([[1, 1], [1, 1], [1, np.nan]], 1))
    [[1. 1.]
     [1. 1.]
     [1. 1.]]
    >>> print(impute_ls([[1, 1], [1, np.nan]], 1))
    [[ 1.  1.]
     [ 1. nan]]
    >>> print(impute_ls([[1, 1], [1, np.nan]]))
    [[ 1.  1.]
     [ 1. nan]]
    """
    A = np.array(A)
    k = A.shape[1]

    if thresh == None:
        thresh = k * 0.2
    elif isinstance(thresh, float):
        thresh *= k

    # Specify rows which may be imputed: 0 < blanks <= thresh
    eligible = np.isnan(A).any(axis=1) & (np.isnan(A).sum(axis=1) <= thresh)
    B = A[eligible]

    # Rows without blanks
    C = A[np.isfinite(A).all(axis=1)]

    if 0 < len(B) < len(C):
        # Move to 3D to calculate for all rows in B concurrently
        # Spend some time to understand how the broadcasting works
        # C.shape (n, k) -> (1, n, k)
        # B.shape (m, k) -> (m, 1, k), where 1 < m < n
        # D.shape (m, n, k)
        D = C[np.newaxis, :] - B[:, np.newaxis]

        # Calculate sum-of-squares along axis=2 (where the k columns are)
        sse = np.nansum(np.square(D), axis=2)

        # Find the row(s) with the minimum sse
        # Average rows if there are ties, avoid using np.argmin()
        E = np.array([C[row == row.min()].mean(axis=0) for row in sse])

        # Impute for specified rows, then replace the original rows
        if rounding:
            F = np.nan_to_num(B) + np.isnan(B) * np.round(E)
        else:
            F = np.nan_to_num(B) + np.isnan(B) * E
        Z = np.copy(A)
        Z[eligible] = F

    # This criteria is rather arbitrary, need to find some literature here...
    elif len(B) >= len(C):
        # print("At least half the rows contain blanks!")
        # print("Perhaps try a different approach?")
        Z = A

    else:
        # print("There is nothing to impute.")
        Z = A

    return Z

if __name__ == "__main__":
    import doctest
    doctest.testmod()
