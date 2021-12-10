#!/usr/bin/env python

from __future__ import annotations

"""
template.py
2021-12-10

...
"""

#%% import-libraries
import argparse
import logging
import sys
import time
import unittest

#%% define-constants
TODAY = time.strftime("%Y-%m-%d")

#%% define-functions
def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, 
        description=__doc__)
    parser.add_argument("-d", "--dry-run", action="store_true", 
        help="dry run")
    parser.add_argument("-t", "--run-tests", action="store_true", 
        help="run tests")
    return parser

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

def timer(f):
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        result = f(*args, **kwargs)
        t2 = time.perf_counter()
        print("Function:", f.__name__)
        print("Arguments:", args, kwargs)
        print("Time taken: {:.6f} secs".format(t2 - t1))
        return result
    return wrapper



class TestMod(unittest.TestCase):

    def test_1(self):
        got = func1(1, 2, 3)
        want = 1, 2, 3
        self.assertEqual(got, want)

    def test_2(self):
        got = func2(4, 5, 6, 7)
        want = 8, 9, 10
        self.assertEqual(got, want)



#%% main
@timer
def main():
    args = setup_parser().parse_args()
    if args.run_tests:
        unittest.main(argv=sys.argv[:1])
        return None

    logger = setup_logger(log_level=args.log_level)

if __name__ == "__main__":
    main()
