# win32-xlsx-template.py

import numpy as np
import pandas as pd
import win32com.client as win32
from pathlib import Path
from time import strftime

def xlsx_template(df, dd, filepath, add_date=True):
    fp = Path(filepath)
    if add_date:
        filename = "{}_{}{}".format(fp.stem, strftime("%Y%m%d"), fp.suffix)
        fp = fp.with_name(filename)

    df = df.reset_index()
    dd = dd.reset_index()

    with pd.ExcelWriter(fp, datetime_format="YYYY-MM-DD") as f:
        df.to_excel(f, sheet_name="Data", index=None, freeze_panes=(1, 1))
        dd.to_excel(f, sheet_name="DataDict", index=None, freeze_panes=(1, 0))

    try:
        xl = win32.gencache.EnsureDispatch("Excel.Application")
        xl.Visible = True
        xl.ScreenUpdating = True
        wb = xl.Workbooks.Open(Path.cwd() / fp)
        s1 = wb.Sheets("Data")
        s2 = wb.Sheets("DataDict")

        s1.Rows(1).HorizontalAlignment = -4131 # xlHAlignLeft
        s1.Rows(1).WrapText = False
        s1.Rows(1).Font.Bold = True
        s1.Columns(1).AutoFit()
        datcols = np.argwhere(df.columns.str.contains("dat")).flatten()
        for i in datcols:
            s1.Columns(i + 1).AutoFit()

        s2.Rows(1).HorizontalAlignment = -4131 # xlHAlignLeft
        s2.Rows(1).Font.Bold = True
        s2.Columns(1).ColumnWidth = 30
        s2.Columns(2).ColumnWidth = 40

    except Exception as e:
        print(e)

    finally:
        s2 = None
        s1 = None
        wb = None
        xl = None
