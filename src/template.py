#!/usr/bin/env python3
# template.py -*- coding: utf-8 -*-
"""
Created on YYYY-MM-DD HH:MM:SS

@author: name
"""

#%% import-libraries
import time

#%% define-functions

#%% main
def main():
    t1 = time.perf_counter()
    
    t2 = time.perf_counter()
    print("Time taken: {:.6f} secs".format(t2 - t1))

if __name__ == "__main__":
    main()
