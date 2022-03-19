#!/usr/bin/env python
#
# util.py
# 2022-03-15

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

def setup_logger(log_level: str="INFO", log_file: str=None) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    log_fmt = "%(asctime)s %(levelname)8s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_fmt, datefmt)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    if log_file is not None:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

def read_db(db_path: str, tables: list|None|str=None) -> dict:
    assert os.path.isfile(db_path)
    with sqlite3.connect(db_path) as conn:
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
    return tbls

def write_csv(dcts: list[dict], path: str, verbose: bool=True) -> None:
    assert os.path.isdir(os.path.dirname(path))
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=dcts[0])
        writer.writeheader()
        writer.writerows(dcts)
    if verbose:
        print(f"File written: '{path}'")

def sqlite_to_csv(
    db_path: str,
    dest_dir: None|str=None,
    verbose: bool=True
) -> None:
    assert os.path.isfile(db_path)
    if dest_dir is None:
        dest_dir = os.path.dirname(db_path)
    else:
        os.makedirs(dest_dir, exist_ok=True)
    tbls = read_db(db_path)
    today = time.strftime("%Y-%m-%d")
    for table_name, tbl in tbls.items():
        filepath = os.path.join(dest_dir, f"{table_name}_{today}.csv")
        write_csv(tbl, filepath)
        if verbose:
            print(f"File written: '{filepath}'")

def main():
    return

    logger = setup_logger()
    logger.info(f"Executing: '{__file__}'")
    dirpath = to_abspath("../data")
    db_path = f"{dirpath}/xnat-dicoms-v4.db"
    csv_dirpath = f"{dirpath}/_csvs"
    sqlite_to_csv(db_path, csv_dirpath)



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
    import unittest

    class TestUtils(unittest.TestCase):
        def test_to_abspath(self):
            self.assertEqual(to_abspath("/a/b/c"), "/a/b/c")
            self.assertTrue(os.path.isabs(to_abspath("./a/b/c")))
            self.assertTrue(os.path.isabs(to_abspath("../a/b/c")))
        def test_setup_logger(self):
            self.assertIsInstance(setup_logger(), logging.Logger)

    unittest.main()

    # main()

