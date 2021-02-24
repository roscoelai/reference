#!/usr/bin/env python3
# template.py -*- coding: utf-8 -*-
"""
Created on YYYY-MM-DD HH:MM:SS

@author: Name
"""

#%% import-libraries
import time

#%% define-functions
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

#%% main
@timer
def main():
    pass

if __name__ == "__main__":
    main()
