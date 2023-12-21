import doctest
import os
import re
from typing import Callable

import numpy as np
import polars as pl
import pyreadstat
import xlsxwriter

def dct_to_redcap_opts(dct: dict[(int | float | str), str]) -> str:
    """
    Convert dictionary mapping values to labels to a string, REDCap format.
    If value is a float, try to convert to int.

    >>> dct_to_redcap_opts({1.0: 'a', 2: 'b', 'NA': 'c, lol', 0.9: 'd 4'})
    '1, a | 2, b | NA, c, lol | 0.9, d 4'
    """
    f2i = lambda x: int(x) if isinstance(x, float) and int(x) == x else x
    return " | ".join(f"{f2i(k)}, {v}" for k, v in dct.items())

def meta_to_dd(meta: pyreadstat.metadata_container) -> pl.DataFrame:
    """
    Convert metadata object to a data dictionary data frame.
    """
    V, D, O = "Variable", "Description", "Options"
    dd = pl.DataFrame({V: meta.column_names, D: meta.column_labels})
    if (vvl := meta.variable_value_labels):
        opts = map(dct_to_redcap_opts, vvl.values())
        dd2 = pl.DataFrame({V: vvl.keys(), O: opts})
        dd = dd.join(dd2, on=V, how="outer_coalesce")
    return dd

def safe_to_int(x: pl.Series | pl.DataFrame) -> pl.Series | pl.DataFrame:
    """
    Convert to int dtype if possible without loss of data.

    >>> safe_to_int(pl.Series([1.0, 2.1])).dtype
    Float64

    >>> safe_to_int(pl.Series([1.0, 2.0])).dtype
    Int64

    >>> safe_to_int(pl.DataFrame({'a': [1.0, 2.1], 'b': [1.0, 2.0]})).dtypes
    [Float64, Int64]

    >>> safe_to_int(pl.DataFrame({'a': [None, None], 'b': [1.0, 2.0]})).dtypes
    [Null, Int64]
    """
    is_ok = lambda s: s.dtype in pl.NUMERIC_DTYPES and s.cast(int).eq(s).all()
    if isinstance(x, pl.Series):
        if is_ok(x):
            x = x.cast(int)
    elif isinstance(x, pl.DataFrame):
        colnames = (s.name for s in x if is_ok(s))
        pattern = f"^({'|'.join(colnames)})$"
        x = x.with_columns(pl.col(pattern).cast(int))
    return x

def read_sav_to_dfdd(path: str) -> (pl.DataFrame, pl.DataFrame):
    df, meta = pyreadstat.read_sav(path)
    df = pl.DataFrame(df).pipe(safe_to_int)
    dd = meta_to_dd(meta)
    return df, dd

def drop_empty_cols(df: pl.DataFrame) -> pl.DataFrame:
    """
    >>> drop_empty_cols(pl.DataFrame({'a': [1], 'b': [2]})).columns
    ['a', 'b']
    
    >>> drop_empty_cols(pl.DataFrame({'a': [1, 2], 'b': [None] * 2})).columns
    ['a']
    """
    assert isinstance(df, pl.DataFrame)
    return df[[s.name for s in df if s.null_count() < df.height]]

def drop_uniform_cols(df: pl.DataFrame) -> pl.DataFrame:
    """
    Remove columns where all values are the same.
    
    >>> drop_uniform_cols(pl.DataFrame({'a': [1, 2], 'b': [3, 4]})).columns
    ['a', 'b']
    
    >>> drop_uniform_cols(pl.DataFrame({'a': [1, 2], 'b': [None] * 2})).columns
    ['a']
    
    >>> drop_uniform_cols(pl.DataFrame({'a': [1, 1], 'b': [3, 4]})).columns
    ['b']
    """
    assert isinstance(df, pl.DataFrame)
    return df[[s.name for s in df if s.dtype != pl.Null and s.n_unique() > 1]]

def drop_empty_rows(df: pl.DataFrame, expr: pl.Expr=pl.all()) -> pl.DataFrame:
    """
    >>> drop_empty_rows(pl.DataFrame({'a': [None, 1], 'b': [2, 3]})).height
    2
    
    >>> drop_empty_rows(pl.DataFrame({'a': [None, 1], 'b': [None, 3]})).height
    1
    """
    assert isinstance(df, pl.DataFrame)
    return df.filter(~pl.all_horizontal(expr.is_null()))

def write_excel_wb(dfs: dict[str, pl.DataFrame], path: str) -> None:
    """
    Write dataframe(s) into an Excel Workbook.
    """
    dd_col_widths = {
        "Variable": 100,
        "Description": 400,
        "Options": 400,
        "Remarks": 100,
    }
    with xlsxwriter.Workbook(path) as wb:
        for k, df in dfs.items():
            cw = dd_col_widths if k.strip().lower() == "datadict" else None
            df.write_excel(workbook=wb,
                           worksheet=k,
                           dtype_formats={pl.INTEGER_DTYPES: "#0"},
                           column_widths=cw)
    print(f"File written: {path}")

# -----------------------------------------------------------------------------

def sav_to_xl(src_path: str, dest_dir: str, func: Callable | None=None) -> None:
    """
    Read a SAV file and write out the corresponding XLSX file.
    The original filename will be retained.
    """
    df, dd = read_sav_to_dfdd(src_path)
    if func:
        df, dd = func(df, dd)
    stem, ext = os.path.splitext(os.path.basename(src_path))
    dest_path = f"{dest_dir}/{stem}.xlsx"
    os.path.isdir(dest_dir) or os.makedirs(dest_dir)
    write_excel_wb({"Data": df, "DataDict": dd}, dest_path)

def savs_to_xls(src_dir: str, dest_dir: str, func: Callable | None=None) -> None:
    for de in os.scandir(src_dir):
        if de.name.endswith(".sav"):
            sav_to_xl(de.path, dest_dir, func)

# -----------------------------------------------------------------------------

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

IMPUTE_FUNC = impute_hd

# -----------------------------------------------------------------------------

def impute_wrapper(df: pl.DataFrame, func: Callable=IMPUTE_FUNC, **kwargs) -> np.ndarray:
    """
    Your responsibilities are:
    - Providing a data frame with only the relevant (usually raw) items
    - Specifying an imputation function
    
    Optional:
    - Items arranged in correct order (the algorithm shouldn't care)
    """
    arr = np.array(df)
    res = func(arr, **kwargs)
    return res

# -----------------------------------------------------------------------------

def main() -> None:
    print(doctest.testmod())

if __name__ == "__main__":
    main()
