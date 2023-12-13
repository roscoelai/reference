import doctest

import polars as pl
import pyreadstat
import xlsxwriter

def dct_to_redcap_opts(dct: dict[int | float | str, str]) -> str:
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

doctest.testmod()
