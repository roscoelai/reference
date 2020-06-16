import numpy as np

def impute_ls(X: np.ndarray, thresh=0.2, rounding=True):
    """
    Imputes missing values using the least squares approach.

    :param X: a matrix of numerical values, may contain missing values
    :param thresh: number or proportion of missing values allowed
    :param rounding: round imputed values to nearest whole number
    :returns: the original matrix with eligible missing values imputed

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
    A = np.array(X)
    k = A.shape[1]

    # Check that thresh is valid
    if isinstance(thresh, int) and (0 <= thresh <= k):
        pass
    elif isinstance(thresh, float) and (0. <= thresh <= 1.):
        thresh *= k
    elif isinstance(thresh, str) and thresh.lower() == "all":
        thresh = k
    else:
        raise ValueError(f"Invalid thresh: {thresh}, {type(thresh)}")

    # Select rows which can be imputed: 0 < nblanks <= thresh
    imputable = np.isnan(A).any(axis=1) & (np.isnan(A).sum(axis=1) <= thresh)
    B = A[imputable]

    # Select rows without blanks, to be used as reference
    C = A[np.isfinite(A).all(axis=1)]

    # There must be more reference rows than rows to impute
    if 0 < len(B) < len(C):
        """
        Move to 3 dimensions to vectorize the entire operation
        Details of broadcasting:
        C (n x k) -> C[np.newaxis, :] (1 x n x k)
        B (m x k) -> B[:, np.newaxis] (m x 1 x k), where 0 < m < n
        D (m x n x k)
        """
        D = C[np.newaxis, :] - B[:, np.newaxis]

        # Calculate sum-of-squares along axis=2 (where the k columns are)
        ss = np.nansum(np.square(D), axis=2)

        # Find the row(s) with the minimum ss (average ties)
        E = np.array([C[rows == rows.min()].mean(axis=0) for rows in ss])
        if rounding:
            E = np.round(E)

        # Impute for specified rows, then replace the original rows
        F = np.nan_to_num(B) + np.isnan(B) * E

        Z = np.copy(A)
        Z[imputable] = F

    elif len(B) >= len(C):
        # print("At least half the rows contain blanks! Process skipped.")
        Z = A

    else:
        # print("There is nothing to impute.")
        Z = A

    return Z

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
