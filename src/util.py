#!/usr/bin/env python
#
# util.py
# 2022-03-13

from __future__ import annotations

import csv
import logging
import os
import sqlite3
import time

def to_abspath(path: str) -> str:
    if os.path.isabs(path):
        return path
    return os.path.realpath(f"__file__/../{path}")
    # return os.path.normpath(os.path.join(__file__, "..", path))

def setup_logger(log_level: str="INFO", log_file: str=None) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    log_fmt = "%(asctime)s %(levelname)8s: %(message)s"
    formatter = logging.Formatter(log_fmt)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file is not None:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

def read_db(db_path: str, tables: list[str]|None|str=None) -> dict[list[dict]]:
    conn = sqlite3.connect(db_path)
    if tables is None:
        sql = "SELECT name FROM sqlite_master WHERE type = 'table';"
        cur = conn.execute(sql)
        tables = cur.fetchone()
    elif isinstance(tables, str):
        tables = [tables]
    tbls = {}
    for table in tables:
        cur = conn.execute(f"SELECT * FROM {table};")
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        tbl = [dict(zip(colnames, row)) for row in rows]
        tbls[table] = tbl
    conn.close()
    return tbls

def write_csv(dcts: list[dict], path: str, verbose: bool=True) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=dcts[0])
        writer.writeheader()
        writer.writerows(dcts)
    if verbose:
        print(f"File written: '{path}'")

def sqlite_to_csv(db_path: str, csv_dirpath: str) -> None:
    tbls = read_db(db_path)
    os.makedirs(csv_dirpath, exist_ok=True)
    today = time.strftime("%Y-%m-%d")
    for table_name, tbl in tbls.items():
        filepath = os.path.join(csv_dirpath, f"{table_name}_{today}.csv")
        write_csv(tbl, filepath)

def main():
    logger = setup_logger()
    logger.info(f"Executing: '{__file__}'")
    # dirpath = to_abspath("../data")
    # db_path = f"{dirpath}/xnat-dicoms-v4.db"
    # csv_dirpath = f"{dirpath}/_csvs"
    # sqlite_to_csv(db_path, csv_dirpath)



# def rename_field(db_path, table, old, new):
#     conn = sqlite3.connect(db_path)
#     with conn:
#         conn.execute(f"ALTER TABLE {table} RENAME COLUMN ? TO ?;", (old, new))
#     cur = conn.execute(f"SELECT * FROM {table};")
#     colnames = [desc[0] for desc in cur.description]
#     print(colnames)
#     conn.close()
# 
# def glimpse(db_path):
#     conn = sqlite3.connect(db_path)
#     cur = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
#     tables = cur.fetchone()
#     for table in tables:
#         print(f"table = {table}")
#         cur.execute(f"SELECT * FROM {table};")
#         colnames = [desc[0] for desc in cur.description]
#         print(f"- colnames = {colnames}")

if __name__ == "__main__":
    main()


