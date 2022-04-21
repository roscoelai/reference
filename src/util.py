#!/usr/bin/env python
#
# util.py
# 2022-04-21
#
# Common utility functions.

from __future__ import annotations

import csv
import getpass
import hashlib
import logging
import netrc
import os
import sqlite3
import tempfile
import time
import urllib
import unittest

def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        t2 = time.perf_counter()
        print("\nFunction:", func.__name__)
        print("Arguments:", args, kwargs)
        print(f"Time taken: {t2 - t1:.6f} secs")
        return result
    return wrapper

def setup_logger(name: str | None=None, log_level: str="INFO", log_file: str | None=None) -> logging.Logger:
    """Setup logger."""
    if name is None:
        name = __name__
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s %(levelname)8s: %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file is not None:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def to_abspath(path: str) -> str:
    """Convert path to absolute path, if not one already."""
    if os.path.isabs(path):
        return path
    return os.path.realpath(f"__file__/../{path}")

def md5sum(x: bytes | str, literal_string: bool=False) -> str:
    """Calculate MD5 sum of string, bytes, or file."""
    if isinstance(x, bytes):
        return hashlib.md5(x).hexdigest()
    elif isinstance(x, str):
        if os.path.isfile(x) and not literal_string:
            with open(x, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        else:
            return hashlib.md5(x.encode()).hexdigest()
    else:
        raise ValueError(f"'{x}' is neither bytes, string, nor file.")

def get_userpass(url: str, user: str=None, passwd: str=None) -> tuple:
    """Get username and password for given URL."""
    if user is None:
        try:
            host = urllib.parse.urlparse(url).netloc
            user, _, passwd = netrc.netrc().authenticators(host)
        except FileNotFoundError as e:
            logger.error(e)
            choice = ""
            while choice not in {"y", "yes"}:
                choice = input("Login manually? [y/n/q]: ").strip().lower()
                if choice in {"n", "q"}:
                    return None, None
            user = input(f"Enter username for '{url}': ")
    if passwd is None:
        passwd = getpass.getpass(f"Enter password for user '{user}': ")
    return user, passwd

def read_db(db_path: str, table_names: list[str] | None=None) -> dict[str, list]:
    """Read tables from SQLite database."""
    with sqlite3.connect(db_path) as conn:
        if table_names is None:
            query = "SELECT name FROM sqlite_master WHERE type = 'table';"
            cur = conn.execute(query)
            table_names = cur.fetchone()
        elif isinstance(table_names, str):
            table_names = [table_names]
        tables = {}
        for table_name in table_names:
            cur = conn.execute(f"SELECT * FROM {table_name};")
            colnames = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            tables[table_name] = [dict(zip(colnames, row)) for row in rows]
        return tables

def write_csv(dcts: list[dict], dest_path: str, verbose: bool=False) -> None:
    """Write a list of dicts to a CSV file."""
    with open(dest_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=dcts[0])
        writer.writeheader()
        writer.writerows(dcts)
    if verbose:
        print(f"File written: '{dest_path}'")

def db_to_csv(db_path: str, csv_dir: str, verbose: bool=False) -> None:
    """Dump tables from SQLite database into CSV files."""
    today = time.strftime("%Y-%m-%d")
    tables = read_db(db_path)
    os.makedirs(csv_dir, exist_ok=True)
    for table_name, rows in tables.items():
        dest_path = os.path.join(csv_dir, f"{table_name}_{today}.csv")
        write_csv(rows, dest_path, verbose=verbose)

def update_db(db_path: str, query: str, dcts: list[dict]) -> None:
    """Update SQLite database based on given query."""
    with sqlite3.connect(db_path) as conn:
        for dct in dcts:
            conn.execute(query, dct)

def rename_field(db_path: str, table_name: str, old: str, new: str, verbose: bool=False) -> None:
    """Rename a field in a table in a SQLite database."""
    with sqlite3.connect(db_path) as conn:
        query = f"ALTER TABLE {table_name} RENAME COLUMN ? TO ?;"
        conn.execute(query, (old, new))
        if verbose:
            cur = conn.execute(f"SELECT * FROM {table_name};")
            colnames = [desc[0] for desc in cur.description]
            print(f"{table_name} colnames: {colnames}")

def seconds_to_dhms(seconds: int | float) -> str:
    """Convert number of seconds to a more human-readable form."""
    sign, days, hours, minutes = "", None, None, None
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    if seconds >= 60:
        minutes, seconds = divmod(seconds, 60)
        if minutes >= 60:
            hours, minutes = divmod(minutes, 60)
            if hours >= 24:
                days, hours = divmod(hours, 24)
    res = f"{seconds:2.3f} s"
    if minutes is not None:
        res = f"{minutes:2.0f} m {res}"
    if hours is not None:
        res = f"{hours:2.0f} h {res}"
    if days is not None:
        res = f"{days:.0f} d {res}"
    return f"{sign}{res}"



@timer
def main() -> None:
    print(f"'\033[93m{__file__}\033[0m' is a module, "
          "and should \033[91mnot\033[0m normally be executed.\n"
          "But since we're here, let's see what functions are available.\n")
    defined_functions = [k for k, v in globals().items() if callable(v)]
    defined_functions = ["Defined functions:"] + defined_functions
    print("\n\033[0m- \033[92m".join(defined_functions), "\033[0m")

if __name__ == "__main__":
    main()

    class TestUtils(unittest.TestCase):

        def test_md5sum(self):
            f = md5sum
            self.assertEqual(f("test1"), "5a105e8b9d40e1329780d62ea2265d8a")
            self.assertEqual(f(b"test2"), "ad0234829205b9033196ba818f7a872b")
            # with tempfile.NamedTemporaryFile() as fp:
            #     fp.write(b"test3")
            #     fp.seek(0)
            #     self.assertEqual(f(fp.name), "8ad8757baa8564dc136c1e07507f4a98")

        def test_seconds_to_dhms(self):
            f = seconds_to_dhms
            self.assertEqual(f(9), "9.000 s")
            self.assertEqual(f(59), "59.000 s")
            self.assertEqual(f(599), " 9 m 59.000 s")
            self.assertEqual(f(3599), "59 m 59.000 s")
            self.assertEqual(f(3600), " 1 h  0 m 0.000 s")
            self.assertEqual(f(40271), "11 h 11 m 11.000 s")
            self.assertEqual(f(86400), "1 d  0 h  0 m 0.000 s")
            self.assertEqual(f(8726399.123), "100 d 23 h 59 m 59.123 s")
            self.assertEqual(f(-9), "-9.000 s")
            self.assertEqual(f(-8726399.123), "-100 d 23 h 59 m 59.123 s")

        
        def test_to_abspath(self):
            f = to_abspath
            self.assertEqual(f("/a/b/c"), "/a/b/c")
            self.assertTrue(os.path.isabs(f("./a/b/c")))
            self.assertTrue(os.path.isabs(f("../a/b/c")))

        def test_setup_logger(self):
            self.assertIsInstance(setup_logger(), logging.Logger)

    print("\nRunning tests:")
    unittest.main()
