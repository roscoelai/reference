#!/usr/bin/env python3
# impute_hd.py

import numpy as np

def impute_hd(A: np.ndarray,
              max_blanks: int | float=0.1,
              round_to_int: bool=True,
              verbose: bool=False) -> np.ndarray:
    """
    Hot deck imputation.

    :param X: a matrix of numerical values, may contain missing values.
    :param max_blanks: number or proportion of missing values allowed per row.
    :param round_to_int: round imputed values to nearest whole number.
    :returns: the original matrix with eligible missing values imputed.

    >>> impute_hd(np.array([[1,      9],
    ...                     [1, np.nan]]), 1)
    array([[ 1.,  9.],
           [ 1., nan]])

    >>> impute_hd(np.array([[1,      2],
    ...                     [1,      9],
    ...                     [1, np.nan]]))
    array([[ 1.,  2.],
           [ 1.,  9.],
           [ 1., nan]])

    >>> impute_hd(np.array([[1,      2],
    ...                     [1,      9],
    ...                     [1, np.nan]]), 1)
    array([[1., 2.],
           [1., 9.],
           [1., 6.]])

    >>> impute_hd(np.array([[ 1,      2,      3],
    ...                     [ 4,      5,      6],
    ...                     [ 7,      8, np.nan],
    ...                     [10, np.nan,     12],
    ...                     [13,     14,     15]]), 1)
    array([[ 1.,  2.,  3.],
           [ 4.,  5.,  6.],
           [ 7.,  8.,  6.],
           [10., 14., 12.],
           [13., 14., 15.]])
    """
    assert isinstance(A, np.ndarray), "Input must be a numpy.ndarray."
    assert not np.isinf(A).any(), "Infinite values not supported."
    _, k = A.shape

    # Check that max_blanks is valid.
    if isinstance(max_blanks, int) and (0 <= max_blanks <= k):
        pass
    elif isinstance(max_blanks, float) and (0.0 <= max_blanks <= 1.0):
        max_blanks *= k
    else:
        msg = f"Invalid max_blanks: {max_blanks = }, {type(max_blanks) = }"
        raise ValueError(msg)

    # Select rows which can be imputed: 0 < n_blanks <= max_blanks.
    n_blanks = np.isnan(A).sum(axis=1)
    imputable = (n_blanks > 0) & (n_blanks <= max_blanks)
    complete = n_blanks == 0
    B = A[imputable]
    C = A[complete]
    n_imputable = len(B)
    n_complete = len(C)

    # Return input unchanged if no imputable rows, or too few complete rows.
    if n_imputable == 0 or n_imputable >= n_complete:
        verbose and print("Nothing imputed. {n_imputable = }, {n_complete = }")
        return A

    """
    Move to 3 dimensions to vectorize the entire operation
    Details of broadcasting:
    C (n x k) -> C[np.newaxis, :] (1 x n x k)
    B (m x k) -> B[:, np.newaxis] (m x 1 x k), where 0 < m < n
    D (m x n x k)
    """
    D = C[np.newaxis, :] - B[:, np.newaxis]  # Takes a while to understand.
    assert D.shape == (n_imputable, n_complete, k)

    # Calculate sum-of-squares along axis=2 (where the k columns are).
    ss = np.nansum(np.square(D), axis=2)
    assert ss.shape == (n_imputable, n_complete)

    # For each imputable row, find the closest row(s) (i.e. minimum ss) among 
    # the complete rows. If there are multiple closest rows, take the average.
    is_min_ss = np.isclose(ss, ss.min(axis=1, keepdims=True))
    E = np.array([C[mask].mean(axis=0) for mask in is_min_ss])
    if round_to_int:
        E = np.round(E)
    assert E.shape == (n_imputable, k)

    # Create imputed rows by filling in blanks with values from closest rows.
    F = np.nan_to_num(B) + np.isnan(B) * E

    # Insert imputed rows into a copy of the original array.
    res = np.copy(A)
    res[imputable] = F
    return res

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
