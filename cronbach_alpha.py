import numpy as np

def cronbach_alpha(X: np.ndarray) -> float:
    """
    Calculates Cronbach's alpha.

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
    ncols = A.shape[1]

    variances_of_columns = np.nanvar(A, axis=0, ddof=1)
    sums_of_rows = np.nansum(A, axis=1)

    sum_of_variances = np.sum(variances_of_columns)
    variance_of_sums = np.var(sums_of_rows, ddof=1)

    prealpha = 1 - (sum_of_variances / variance_of_sums)
    alpha = ncols / (ncols - 1) * prealpha

    return alpha

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
