"""
columnranker
============

Original Problem:
- Suppose we have a few tables of data that we wish to merge
- Suppose that each table has few/no missing values
- All tables have a set of IDs (aka index, rownames, etc.)
- The IDs in each table are a subset of a universal set of IDs
- The set of IDs for each table could be very different
- When we INNER JOIN 2 tables, we take the intersection of their IDs
- In the worst case, there are no common IDs, we end up with an empty table
- Qn: Which tables should we join together to maximize the number of rows?

Modified Problem:
- Change "table" above to "column"
- We could think of columns of different lengths, all without missing values
- Or we could have columns of the same length, but different number of blanks
- It makes no difference
- We have a bunch of columns
- Qn: Which columns should we join together to maximize...
- ... number of rows?
  - Well, just take the column with the most values on its own (no joins)!
- ... number of columns?
  - Well, just join ALL the columns!
- ... how about (number of rows) * (number of columns)?
  - Adding columns would increase the number of columns
  - Adding columns would maintain or reduce the number of rows (never increase)
  - This might just be optimizable!
  - Let's call this score = nrows*ncols
- We just have to calculate the score for every combination of columns
- Then we find the maximum score and the corresponding combination of columns
- Then we are done!

TIME TO WAKE UP!

- How many combinations are there to calculate?
- nC1 + nC2 + nC3 + ... + nC(n-2) + nC(n-1) + nCn
- By the binomial theorem, there are 2^n - 1 combinations
- For n = 98 columns, there will be 2^98 - 1 scores to calculate
- That is 316,912,650,057,057,350,374,175,801,343
- Suppose the computer has unlimited memory
- Suppose each calculation takes 1 nanosecond
- It would take 10,042,355,884,384 years to complete the calculation!
- This problem is NP-hard, and the naive approach is impractical
- It's easy to calculate scores, but there's just too many to try

We have to use heuristics here:
- i.e. we abandon any guarantees of finding the "best" combination of columns
- We significantly change the problem statement

Very Modified Problem:
A: I have a bunch of columns.
A: Which one is the "best"?
B: What do you mean by "best"?
A: I want to maximize nrows*ncols, eventually.
B: The column with the most values! (<-- method_1)
A: But that column has no IDs in common with the others!
A: If we INNER JOIN with the other columns, we'll get an empty table.
B: It can't be the "best", then.
B: So, the relationship between columns is important.
B: We could INNER JOIN pairs of columns,
B: then calculate the rowcount of each pair. (<-- method_2)
B: We cross tabulate all the scores into a symmetric, n x n matrix.
B: That column mentioned previously would score 0 for all combinations,
B: except with itself.
A: So which is the "best" column?
B: We can sum the rowcounts for each column.
B: That would give it a score relative to the other columns.
B: The "best" column would have the highest score.
B: This way, the "best" column is determined by how well it does with others.
A: Why not consider groups of 3 columns? (<-- method_3)
B: Sure! However, the cross-tabulation is now 3-dimensional and less intuitive.
A: How about groups of 4 columns? (<-- method_4)
B: It would take much longer, and the cross-tabulation is 4-dimensional.
A: Groups of 5 columns?
B: Don't push your luck...
A: Why not groups of n columns?
B: That's ideal, but there are 2^n - 1 groups...

- Each approach is a scoring scheme that will score all columns
- The scores can be used to rank the columns, yielding a "best" sequence
- That is, the "best" order to add columns while minimizing rows lost
- Different scoring schemes may produce different orderings
- For any table, calculating the number of rows with no blanks is easy
- The column order can be visualized with a "survival curve"



There are currently 4 working functions defined in this module:

method_1:
- Evaluates columns individually; Count number of values per column
- Scores returned in a 1-D vector

method_2:
- Evaluates columns in pairs; Count number of aligned rows in each pair
- Scores returned in a 2-D matrix (square, n x n)
- Aggregated to a 1-D vector by summing along axis 0

method_3:
- Evaluates columns in groups of 3; Count number of aligned rows in each group
- Score returned in a 3-D tensor (cube, n x n x n)
- Aggregated to a n x n square by summing along axis 0
- Aggregated to a 1-D vector by summing along axis 0

method_4:
- Evaluates columns in groups of 4; Count number of aligned rows in each group
- Score returned in a 4-D tensor (tesseract, n x n x n x n)
- Aggregated to a n x n x n cube by summing along axis 0
- Aggregated to a n x n square by summing along axis 0
- Aggregated to a 1-D vector by summing along axis 0

method_5:
- Crashes Python



Another approch to consider is dynamic programming
- Time to revisit some bioinformatics...

Last updated: 24 May 2020
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from numba import jit
from timeit import default_timer as timer

class ColumnRanker:
    def __init__(self, wide_df):
        self.df = wide_df
        self.get_all_ranks()

    def get_all_ranks(self):
        methods = {
            "method_1": method_1,
            "method_2": method_2,
            "method_3": method_3,
            "method_4": method_4,
        }
        A = self.df.notna().astype(int).values

        scores = {}
        dfs = {}
        cumulatives = {}
        singulars = {}
        timings = {}
        for k, method in methods.items():
            print(f"Calculating {k}... ", end="")
            start = timer()

            scores[k] = pd.Series(method(A), index=self.df.columns)
            dfs[k] = df = self.df[sorted(self.df, key=lambda x: scores[k][x], reverse=True)].notna()
            cumulatives[k] = pd.Series({k: df.loc[:, :k].all(axis=1).sum() for k in df}, name="cumulative")
            singulars[k] = pd.Series({k: s.sum() for k, s in df.items()}, name="singular")

            end = timer()
            timings[k] = end - start
            print(f"Done! Time taken: {timings[k]:.3f} s")

        self.scores = scores
        self.dfs = dfs
        self.cumulatives = cumulatives
        self.singulars = singulars
        self.timings = timings

    def viz_all(self):
        for k in self.dfs:
            self.viz_survival(k)
        self.viz_overlay()
        plt.show()

    def viz_survival(self, method):
        cumulative = self.cumulatives[method]
        singular = self.singulars[method]
        timing = self.timings[method]

        with plt.style.context("seaborn-whitegrid"):
            fig, ax = plt.subplots(figsize=(18, 8), tight_layout=True)
            ax.plot(cumulative, "bx-", label="Cumulative count")
            ax.plot(singular, "gx", label="Singular count")
            ax.set(title=f"{method}: {timing:.3f} s", ylabel="Number of complete rows")
            ax.legend()
            plt.axhline(100, linewidth=1, color="r", alpha=0.7)
            plt.xticks(rotation=90)
        return ax

    def viz_overlay(self):
        x = range(1, self.df.shape[1] + 1)
        with plt.style.context("seaborn-whitegrid"):
            fig, ax = plt.subplots(figsize=(18, 8), tight_layout=True)
            for k, cumulative in self.cumulatives.items():
                ax.plot(x, cumulative, "x-", label=f"{k} - {self.timings[k]:.3f} s", alpha=0.6)
            ax.set(title="Rows available following sequential addition of columns", ylabel="Number of complete rows", xlabel="Number of columns")
            ax.legend()
            plt.axhline(100, linewidth=1, color="r", alpha=0.5)
        return ax



def method_1(A):
    """Consider individual columns

    Limitation: Does not consider relationship with other columns. A column 
                with many values may have few/no IDs in common with other rows. 
                Merging with this column may yield an empty table.
    """
    return A.sum(axis=0)

def method_2(A):
    "Consider pairs of columns"
    return (A.T @ A).sum(axis=0)

@jit(nopython=True)
def method_3(A):
    "Consider groups of three columns"
    ncol = A.shape[1]
    B = np.empty(shape=(ncol, ncol, ncol))
    for i in range(ncol):
        for j in range(i, ncol):
            for k in range(j, ncol):
                B[i, j, k] = B[i, k, j] = \
                B[j, i, k] = B[j, k, i] = \
                B[k, i, j] = B[k, j, i] = \
                (A[:, i] & A[:, j] & A[:, k]).sum()
    return B.sum(axis=0).sum(axis=0)

@jit(nopython=True)
def method_4(A):
    "Consider groups of four columns"
    ncol = A.shape[1]
    B = np.empty(shape=(ncol, ncol, ncol, ncol))
    for i in range(ncol):
        for j in range(i, ncol):
            for k in range(j, ncol):
                for l in range(k, ncol):
                    B[i, j, k, l] = B[i, j, l, k] = B[i, k, j, l] = B[i, k, l, j] = B[i, l, j, k] = B[i, l, k, j] = \
                    B[j, i, k, l] = B[j, i, l, k] = B[j, k, i, l] = B[j, k, l, i] = B[j, l, i, k] = B[j, l, k, i] = \
                    B[k, i, j, l] = B[k, i, l, j] = B[k, j, i, l] = B[k, j, l, i] = B[k, l, i, j] = B[k, l, j, i] = \
                    B[l, i, j, k] = B[l, i, k, j] = B[l, j, i, k] = B[l, j, k, i] = B[l, k, i, j] = B[l, k, j, i] = \
                    (A[:, i] & A[:, j] & A[:, k] & A[:, l]).sum()
    return B.sum(axis=0).sum(axis=0).sum(axis=0)

@jit(nopython=True)
def method_5(A):
    """Keep this around for future development

    *** DO NOT USE ***

    """
    ncol = A.shape[1]
    B = np.empty(shape=(ncol, ncol, ncol, ncol, ncol))
    for i in range(ncol):
        for j in range(i, ncol):
            for k in range(j, ncol):
                for l in range(k, ncol):
                    for m in range(l, ncol):
                        B[i, j, k, l, m] = B[i, j, k, m, l] = B[i, j, l, k, m] = B[i, j, l, m, k] = B[i, j, m, k, l] = B[i, j, m, l, k] = \
                        B[i, k, j, l, m] = B[i, k, j, m, l] = B[i, k, l, j, m] = B[i, k, l, m, j] = B[i, k, m, j, l] = B[i, k, m, l, j] = \
                        B[i, l, j, k, m] = B[i, l, j, m, k] = B[i, l, k, j, m] = B[i, l, k, m, j] = B[i, l, m, j, k] = B[i, l, m, k, j] = \
                        B[i, m, j, k, l] = B[i, m, j, l, k] = B[i, m, k, j, l] = B[i, m, k, l, j] = B[i, m, l, j, k] = B[i, m, l, k, j] = \
                        B[j, i, k, l, m] = B[j, i, k, m, l] = B[j, i, l, k, m] = B[j, i, l, m, k] = B[j, i, m, k, l] = B[j, i, m, l, k] = \
                        B[j, k, i, l, m] = B[j, k, i, m, l] = B[j, k, l, i, m] = B[j, k, l, m, i] = B[j, k, m, i, l] = B[j, k, m, l, i] = \
                        B[j, l, i, k, m] = B[j, l, i, m, k] = B[j, l, k, i, m] = B[j, l, k, m, i] = B[j, l, m, i, k] = B[j, l, m, k, i] = \
                        B[j, m, i, k, l] = B[j, m, i, l, k] = B[j, m, k, i, l] = B[j, m, k, l, i] = B[j, m, l, i, k] = B[j, m, l, k, i] = \
                        B[k, i, j, l, m] = B[k, i, j, m, l] = B[k, i, l, j, m] = B[k, i, l, m, j] = B[k, i, m, j, l] = B[k, i, m, l, j] = \
                        B[k, j, i, l, m] = B[k, j, i, m, l] = B[k, j, l, i, m] = B[k, j, l, m, i] = B[k, j, m, i, l] = B[k, j, m, l, i] = \
                        B[k, l, i, j, m] = B[k, l, i, m, j] = B[k, l, j, i, m] = B[k, l, j, m, i] = B[k, l, m, i, j] = B[k, l, m, j, i] = \
                        B[k, m, i, j, l] = B[k, m, i, l, j] = B[k, m, j, i, l] = B[k, m, j, l, i] = B[k, m, l, i, j] = B[k, m, l, j, i] = \
                        B[l, i, j, k, m] = B[l, i, j, m, k] = B[l, i, k, j, m] = B[l, i, k, m, j] = B[l, i, m, j, k] = B[l, i, m, k, j] = \
                        B[l, j, i, k, m] = B[l, j, i, m, k] = B[l, j, k, i, m] = B[l, j, k, m, i] = B[l, j, m, i, k] = B[l, j, m, k, i] = \
                        B[l, k, i, j, m] = B[l, k, i, m, j] = B[l, k, j, i, m] = B[l, k, j, m, i] = B[l, k, m, i, j] = B[l, k, m, j, i] = \
                        B[l, m, i, j, k] = B[l, m, i, k, j] = B[l, m, j, i, k] = B[l, m, j, k, i] = B[l, m, k, i, j] = B[l, m, k, j, i] = \
                        B[m, i, j, k, l] = B[m, i, j, l, k] = B[m, i, k, j, l] = B[m, i, k, l, j] = B[m, i, l, j, k] = B[m, i, l, k, j] = \
                        B[m, j, i, k, l] = B[m, j, i, l, k] = B[m, j, k, i, l] = B[m, j, k, l, i] = B[m, j, l, i, k] = B[m, j, l, k, i] = \
                        B[m, k, i, j, l] = B[m, k, i, l, j] = B[m, k, j, i, l] = B[m, k, j, l, i] = B[m, k, l, i, j] = B[m, k, l, j, i] = \
                        B[m, l, i, j, k] = B[m, l, i, k, j] = B[m, l, j, i, k] = B[m, l, j, k, i] = B[m, l, k, i, j] = B[m, l, k, j, i] = \
                        (A[:, i] & A[:, j] & A[:, k] & A[:, l] & A[:, m]).sum()
    return B.sum(axis=0).sum(axis=0).sum(axis=0).sum(axis=0)
