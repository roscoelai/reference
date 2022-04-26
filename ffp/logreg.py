#!/usr/bin/env python
#
# logreg.py
# 2022-04-26

# TODO(roscoelai): Normalize dataset before optimization
# TODO(roscoelai): Multi-record test cases

from __future__ import annotations

import math
import random
import unittest
from typing import Callable

class LogReg():
    def __init__(
        self,
        w: list[float] | None=None,
        n: int | None=None,
        activation: Callable | None=None,
        loss_fn: Callable | None=None,
        learning_rate: float=0.5,
        threshold: float=1e-5
    ):
        if w is None and n is not None:
            random.seed(42)
            self.w = [random.random() for _ in range(n)]
        else:
            self.w = w
        if activation is None:
            self.activation = self.sigmoid
            self.activation_grad_fn = self.sigmoid_grad
        if loss_fn is None:
            self.loss_fn = self.bce
            self.loss_grad_fn = self.bce_grad
        self.learning_rate = learning_rate
        self.threshold = threshold

    @classmethod
    def sigmoid(self, x: float) -> float:
        """Domain: (-Inf, Inf), Range: (0, 1)"""
        return 1 / (1 + math.exp(-x))

    @classmethod
    def sigmoid_grad(self, g: float) -> float:
        """Domain: (0, 1), Range: (0, 0.25]"""
        return g * (1 - g)

    @classmethod
    def bce(self, g: float, y: int) -> float:
        """Domain: (0, 1), Range: (0, Inf)"""
        return -(y * math.log(g) + (1 - y) * math.log(1 - g))

    @classmethod
    def bce_grad(self, g: float, y: int) -> float:
        """Domain: (0, 1), Range: (-Inf, -1) if y == 1, (1, Inf) if y == 0"""
        return ((1 - y) / (1 - g)) - (y / g)

    @classmethod
    def dotprod(self, x: list[float], y: list[float]) -> float:
        """Dot (inner) product."""
        assert len(x) == len(y)
        return sum(x_i * y_i for x_i, y_i in zip(x, y))

    @classmethod
    def matmul(self, x: list[list[float]], y: list[list[float]]) -> list[list[float]]:
        """Matrix multiplication."""
        assert len(x[0]) == len(y)
        return [[self.dotprod(x_i, y_j) for y_j in zip(*y)] for x_i in x]

    def calc_z(self, x: list[list[float]], w: list | None=None) -> list[float]:
        """x: (n x m), x1: (n x (m+1)), w: ((m+1) x k), z: (n x k), k = 1"""
        x1 = [[1] + list(x_i) for x_i in x]
        if w is None:
            w = self.w
        if isinstance(w[0], (float, int)):
            w = [[w_j] for w_j in self.w]
        z = self.matmul(x1, w)
        self.z = list(next(zip(*z)))  # k = 1
        return self.z

    def calc_g(self, z: list[float] | None=None) -> list[float]:
        """z: (n x k), g: (n x k), k = 1"""
        if z is None:
            z = self.z
        g = [self.activation(z_i) for z_i in z]
        self.g = g
        return self.g

    def calc_loss(self, y: list[int], g: list[float] | None=None) -> list[float]:
        """y: (n x 1), g: (n x k), k = 1"""
        if g is None:
            g = self.g
        self.loss = [self.loss_fn(g_i, y_i) for g_i, y_i in zip(g, y)]
        return self.loss

    def calc_grad_loss(self, y: list[int], g: list[float] | None=None) -> list[float]:
        """y: (n x 1), g: (n x k), k = 1"""
        if g is None:
            g = self.g
        self.grad_loss = [self.loss_grad_fn(g_i, y_i) for g_i, y_i in zip(g, y)]
        return self.grad_loss

    def calc_grad_activation(self, g: list[float] | None=None) -> list[float]:
        """g: (n x k), k = 1"""
        if g is None:
            g = self.g
        self.grad_activation = [self.activation_grad_fn(g_i) for g_i in g]
        return self.grad_activation

    def calc_grads(self, x: list[list[float]], y: list[int], g: list[float] | None=None) -> list[list[float]]:
        """x: (n x m), y: (n x 1), g: (n x k), k = 1"""
        if g is None:
            g = self.g
        dL_dgs = self.calc_grad_loss(y, g)
        dg_dzs = self.calc_grad_activation(g)
        common_terms = [dL_dg * dg_dz for dL_dg, dg_dz in zip(dL_dgs, dg_dzs)]
        all_grads = []
        for common_term, x_i in zip(common_terms, x):
            grads = [common_term]
            for x_ij in x_i:
                grads.append(common_term * x_ij)
            all_grads.append(grads)
        self.grads = all_grads
        return self.grads

    def update_w(self, grads: list[list[float]] | None=None, learning_rate: float | None=None) -> None:
        if grads is None:
            grads = self.grads
        if learning_rate is None:
            learning_rate = self.learning_rate
        for i, _ in enumerate(self.w):
            grads_t = list(zip(*grads))[i]
            mean_grad = sum(grads_t) / len(grads_t)
            self.w[i] -= mean_grad * learning_rate

    def predict(self, x: list[list[float]]) -> list[float]:
        z = self.calc_z(x)
        g = self.calc_g(z)
        return g

    def fit(self, x: list[list[float]], y: list[int], learning_rate: float | None=None, threshold: float | None=None, max_cycles: int | None=None) -> int:
        if learning_rate is None:
            learning_rate = self.learning_rate
        if threshold is None:
            threshold = self.threshold
        if max_cycles is None:
            max_cycles = 10000
        cycles = 0
        while True:
            g = self.predict(x)
            loss = self.calc_loss(y, g)
            if sum(loss) < threshold:
                self.cycles = cycles
                return cycles
            grads = self.calc_grads(x, y, g)
            self.update_w(grads, learning_rate)
            cycles += 1
            if cycles >= max_cycles:
                self.cycles = cycles
                return cycles

class TestLogReg(unittest.TestCase):
    def setUp(self):
        self.lr1 = LogReg([1, 2, 3])

    def test_init_params(self):
        lr = LogReg([1, 2, 3])
        self.assertEqual(lr.w, [1, 2, 3])

    def test_sigmoid(self):
        self.assertEqual(LogReg.sigmoid(-math.log(7)), 0.12500000000000003)
        self.assertEqual(LogReg.sigmoid(-math.log(4)), 0.2)
        self.assertEqual(LogReg.sigmoid(-math.log(3)), 0.25)
        self.assertEqual(LogReg.sigmoid(0), 0.5)
        self.assertEqual(LogReg.sigmoid(math.log(3)), 0.75)
        self.assertEqual(LogReg.sigmoid(math.log(4)), 0.8)
        self.assertEqual(LogReg.sigmoid(math.log(7)), 0.875)

    def test_sigmoid_grad(self):
        self.assertEqual(LogReg.sigmoid_grad(0), 0)
        self.assertEqual(LogReg.sigmoid_grad(0.25), 0.1875)
        self.assertEqual(LogReg.sigmoid_grad(0.5), 0.25)
        self.assertEqual(LogReg.sigmoid_grad(0.75), 0.1875)
        self.assertEqual(LogReg.sigmoid_grad(1), 0)

    def test_bce(self):
        self.assertEqual(LogReg.bce(0.9999, 1), 0.00010000500033334732)
        self.assertEqual(LogReg.bce(0.999, 1), 0.0010005003335835344)
        self.assertEqual(LogReg.bce(0.5, 1), math.log(2))
        self.assertEqual(LogReg.bce(0.001, 1), 6.907755278982137)
        self.assertEqual(LogReg.bce(0.0001, 1), 9.210340371976182)
        self.assertEqual(LogReg.bce(0.9999, 0), 9.210340371976294)
        self.assertEqual(LogReg.bce(0.999, 0), 6.907755278982136)
        self.assertEqual(LogReg.bce(0.5, 0), math.log(2))
        self.assertEqual(LogReg.bce(0.001, 0), 0.0010005003335835344)
        self.assertEqual(LogReg.bce(0.0001, 0), 0.00010000500033334732)

    def test_bce_grad(self):
        self.assertEqual(LogReg.bce_grad(0.999, 1), -1.001001001001001)
        self.assertEqual(LogReg.bce_grad(0.5, 1), -2)
        self.assertEqual(LogReg.bce_grad(0.001, 1), -1000)
        self.assertEqual(LogReg.bce_grad(0.999, 0), 999.9999999999991)
        self.assertEqual(LogReg.bce_grad(0.5, 0), 2)
        self.assertEqual(LogReg.bce_grad(0.001, 0), 1.001001001001001)

    def test_dotprod(self):
        self.assertEqual(LogReg.dotprod([1, 2, 3], [4, 5, 6]), 32)

    def test_matmul(self):
        self.assertEqual(LogReg.matmul([[1, 2, 3], [4, 5, 6]], [[1], [2], [3]]), [[14], [32]])
        self.assertEqual(LogReg.matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]])

    def test_calc_z(self):
        lr = LogReg([1, 2, 3])
        self.assertEqual(lr.calc_z([[4, 5]]), [24])
        lr = LogReg([1, 2, 3, 4])
        self.assertEqual(lr.calc_z([[4, 5, 6]]), [48])
        lr = LogReg([1, 2, 3])
        self.assertEqual(lr.calc_z([[4, 5], [6, 7]]), [24, 34])

    def test_calc_g(self):
        lr = LogReg()
        self.assertEqual(lr.calc_g([math.log(1)]), [0.5])

    def test_calc_loss(self):
        if not hasattr(self.lr1, "g"):
            self.lr1.calc_g(self.lr1.calc_z([[4, 5]]))
        self.assertEqual(self.lr1.calc_loss([1]), [3.775135759625163e-11])
        self.assertEqual(self.lr1.calc_loss([0]), [23.999999678084425])

    def test_calc_grad_loss(self):
        if not hasattr(self.lr1, "g"):
            self.lr1.calc_g(self.lr1.calc_z([[4, 5]]))
        self.assertEqual(self.lr1.calc_grad_loss([1]), [-1.0000000000377514])
        self.assertEqual(self.lr1.calc_grad_loss([0]), [26489113602.583836])

    def test_calc_grads(self):
        x = [[4, 5]]
        if not hasattr(self.lr1, "g"):
            self.lr1.predict(x)
        y = [1]
        self.lr1.calc_grads(x, y)
        self.assertEqual(self.lr1.grads[0][0], -3.775135759553905e-11)
        self.assertEqual(self.lr1.grads[0][1], -1.510054303821562e-10)
        self.assertEqual(self.lr1.grads[0][2], -1.8875678797769524e-10)
        y = [0]
        self.lr1.calc_grads(x, y)
        self.assertEqual(self.lr1.grads[0][0], 0.9999999999622485)
        self.assertEqual(self.lr1.grads[0][1], 3.999999999848994)
        self.assertEqual(self.lr1.grads[0][2], 4.9999999998112425)

    def test_after_1_round(self):
        x = [[4, 5]]
        y = [0]
        self.assertEqual(self.lr1.w[0], 1)
        self.assertEqual(self.lr1.w[1], 2)
        self.assertEqual(self.lr1.w[2], 3)
        self.assertEqual(self.lr1.predict(x), [0.9999999999622486])
        self.lr1.calc_grads(x, y)
        self.lr1.update_w(learning_rate=0.5)
        self.assertEqual(self.lr1.w[0], 0.5000000000188758)
        self.assertEqual(self.lr1.w[1], 7.550293723568302e-11)
        self.assertEqual(self.lr1.w[2], 0.5000000000943787)
        self.assertEqual(self.lr1.predict(x), [0.9525741268582485])

    def test_after_2_rounds(self):
        x = [[4, 5]]
        y = [0]
        self.assertEqual(self.lr1.predict(x), [0.9999999999622486])
        for _ in range(2):
            self.lr1.calc_grads(x, y)
            self.lr1.update_w(learning_rate=0.5)
        self.assertEqual(self.lr1.w[0], 3.775152412899274e-11)
        self.assertEqual(self.lr1.w[1], -1.9999999998489941)
        self.assertEqual(self.lr1.w[2], -1.9999999998112425)
        self.assertEqual(self.lr1.predict(x), [1.5229979536908425e-08])

    def test_after_2_rounds_slow_learner(self):
        x = [[4, 5]]
        y = [0]
        self.assertEqual(self.lr1.predict(x), [0.9999999999622486])
        for _ in range(2):
            self.lr1.calc_grads(x, y)
            self.lr1.update_w(learning_rate=0.27)
        self.assertEqual(self.lr1.w[0], 0.4600000000203858)
        self.assertEqual(self.lr1.w[1], -0.15999999991845693)
        self.assertEqual(self.lr1.w[2], 0.30000000010192895)
        self.assertEqual(self.lr1.predict(x), [0.7891817066647028])

    def test_after_5_rounds_slow_learner(self):
        x = [[4, 5]]
        y = [0]
        self.assertEqual(self.lr1.predict(x), [0.9999999999622486])
        for _ in range(5):
            self.lr1.calc_grads(x, y)
            self.lr1.update_w(learning_rate=0.12)
        self.assertEqual(self.lr1.w[0], 0.4000000000226508)
        self.assertEqual(self.lr1.w[1], -0.3999999999093965)
        self.assertEqual(self.lr1.w[2], 1.1325429483122207e-10)
        self.assertEqual(self.lr1.predict(x), [0.23147521667021978])

    def test_predict(self):
        x = [[4, 5]]
        self.assertEqual(self.lr1.predict(x), [LogReg.sigmoid(24)])

    def test_fit_1(self):
        x = [[4, 5]]
        y = [0]
        self.assertEqual(self.lr1.w[0], 1)
        self.assertEqual(self.lr1.w[1], 2)
        self.assertEqual(self.lr1.w[2], 3)
        self.assertEqual(self.lr1.predict(x), [0.9999999999622486])
        self.lr1.fit(x, y)
        self.assertEqual(self.lr1.cycles, 2)
        self.assertEqual(self.lr1.w[0], 0.023712936589751543)
        self.assertEqual(self.lr1.w[1], -1.905148253640994)
        self.assertEqual(self.lr1.w[2], -1.8814353170512423)
        self.assertEqual(self.lr1.predict(x), [4.123177234119961e-08])

    def test_fit_2(self):
        x = [[4, 5], [6, 7]]
        y = [0, 0]
        self.assertEqual(self.lr1.w[0], 1)
        self.assertEqual(self.lr1.w[1], 2)
        self.assertEqual(self.lr1.w[2], 3)
        self.assertEqual(self.lr1.predict(x), [0.9999999999622486, 0.9999999999999982])
        self.lr1.fit(x, y)
        self.assertEqual(self.lr1.cycles, 9447)
        self.assertEqual(self.lr1.w[0], 0.27170766819206177)
        self.assertEqual(self.lr1.w[1], -1.460914619181487)
        self.assertEqual(self.lr1.w[2], -1.1892069509894383)
        self.assertEqual(self.lr1.predict(x), [9.949427830113722e-06, 4.9651921143642956e-08])

    def test_fit_3(self):
        x = [[4, 5], [6, 7]]
        y = [0, 1]
        self.assertEqual(self.lr1.w[0], 1)
        self.assertEqual(self.lr1.w[1], 2)
        self.assertEqual(self.lr1.w[2], 3)
        self.assertEqual(self.lr1.predict(x), [0.9999999999622486, 0.9999999999999982])
        self.lr1.fit(x, y)
        self.assertEqual(self.lr1.cycles, 10000)
        self.assertEqual(self.lr1.w[0], -20.11666097319304)
        self.assertEqual(self.lr1.w[1], 12.817878829664442)
        self.assertEqual(self.lr1.w[2], -7.298782143528555)
        self.assertEqual(self.lr1.predict(x), [0.004777464629813595, 0.9966623231217798])



def main() -> None:
    unittest.main()

if __name__ == "__main__":
    main()



