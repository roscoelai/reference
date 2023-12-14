import doctest
import os
from typing import Callable

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
        dd = dd.join(dd2, on=V, how="outer")
    return dd

def safe_to_int(df: pl.DataFrame) -> pl.DataFrame:
    """
    Convert columns to int dtype if possible without loss of data.

    >>> safe_to_int(pl.DataFrame({'a': [1.0, 2.1], 'b': [1.0, 2.0]})).dtypes
    [Float64, Int64]

    >>> safe_to_int(pl.DataFrame({'a': [None, None], 'b': [1.0, 2.0]})).dtypes
    [Int64, Int64]
    """
    assert isinstance(df, pl.DataFrame)
    is_ok = lambda s: s.dtype in pl.NUMERIC_DTYPES and s.cast(int).eq(s).all()
    pattern = f"^({'|'.join(s.name for s in df if is_ok(s))})$"
    df = df.with_columns(pl.col(pattern).cast(int))
    return df

def read_sav_to_dfdd(path: str) -> (pl.DataFrame, pl.DataFrame):
    df, meta = pyreadstat.read_sav(path)
    df = pl.DataFrame(df).pipe(safe_to_int)
    dd = meta_to_dd(meta)
    return df, dd

def drop_empty_cols(df: pl.DataFrame) -> pl.DataFrame:
    assert isinstance(df, pl.DataFrame)
    return df[[s.name for s in df if s.null_count() < df.height]]

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

doctest.testmod()
