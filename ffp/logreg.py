#!/usr/bin/env python
#
# logreg.py
# 2022-04-25

# TODO(roscoelai): Understand what's going on
# TODO(roscoelai): Design and implement API for `fit()`
# TODO(roscoelai): Handle more than one record
# TODO(roscoelai): Normalize dataset before optimization

from __future__ import annotations

import math
import random
import unittest
from typing import Callable

class LogReg():
    def __init__(
        self,
        w: list[float] | None=None,
        activation: Callable | None=None,
        loss_fn: Callable | None=None,
        learning_rate: float | None=None
    ):
        if w is None:
            random.seed(42)
            self.w = [random.random() for _ in range(3)]
        else:
            self.w = w
        if activation is None:
            self.activation = self.sigmoid
            self.activation_grad_fn = self.calc_grad_sigmoid
        if loss_fn is None:
            self.loss_fn = self.bce
            self.loss_grad_fn = self.calc_grad_bce
        if learning_rate is None:
            learning_rate = 0.5

    @classmethod
    def sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-x))

    @classmethod
    def bce(self, g: float, y: int) -> float:
        return -(y * math.log(g) + (1 - y) * math.log(1 - g))

    @classmethod
    def calc_grad_bce(self, g: float, y: int) -> float:
        return ((1 - y) / (1 - g)) - (y / g)

    @classmethod
    def calc_grad_sigmoid(self, g: float) -> float:
        return g * (1 - g)

    def calc_z(self, x: list[float]) -> float:
        self.z = sum(_w * _x for _w, _x in zip(self.w, [1] + list(x)))
        return self.z

    def calc_g(self, z: float) -> float:
        self.g = self.activation(z)
        return self.g

    def calc_loss(self, y: int) -> float:
        self.loss = self.loss_fn(self.g, y)
        return self.loss

    def calc_grad_loss(self, y: int) -> float:
        self.grad_loss = self.loss_grad_fn(self.g, y)
        return self.grad_loss

    def calc_grad_activation(self) -> float:
        self.grad_activation = self.activation_grad_fn(self.g)
        return self.grad_activation

    def calc_grads(self, y: int, x: list[float]=None) -> float:
        common_term = self.calc_grad_loss(y) * self.calc_grad_activation()
        grads = [common_term]
        for _x in x:
            grads.append(common_term * _x)
        self.grads = grads
        return grads

    def update_w(self, learning_rate: float) -> None:
        for i, _ in enumerate(self.w):
            self.w[i] -= self.grads[i] * learning_rate

    def predict(self, x: list[float]) -> float:
        z = self.calc_z(x)
        g = self.calc_g(z)
        return g

class TestLogReg(unittest.TestCase):
    def setUp(self):
        w = [1, 2, 3]
        lr = LogReg(w)
        x = 4, 5
        z = lr.calc_z(x)
        g = lr.calc_g(z)
        self.lr = lr

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

    def test_bce(self):
        self.assertEqual(LogReg.bce(0.9999, 1), 0.00010000500033334732)
        self.assertEqual(LogReg.bce(0.999, 1), 0.0010005003335835344)
        self.assertEqual(LogReg.bce(0.999, 0), 6.907755278982136)
        self.assertEqual(LogReg.bce(0.5, 1), math.log(2))
        self.assertEqual(LogReg.bce(0.5, 0), math.log(2))
        self.assertEqual(LogReg.bce(0.001, 0), 0.0010005003335835344)
        self.assertEqual(LogReg.bce(0.001, 1), 6.907755278982137)
        self.assertEqual(LogReg.bce(0.0001, 0), 0.00010000500033334732)

    def test_calc_grad_bce(self):
        self.assertEqual(LogReg.calc_grad_bce(0.999, 1), -1.001001001001001)
        self.assertEqual(LogReg.calc_grad_bce(0.999, 0), 999.9999999999991)
        self.assertEqual(LogReg.calc_grad_bce(0.5, 1), -2)
        self.assertEqual(LogReg.calc_grad_bce(0.5, 0), 2)
        self.assertEqual(LogReg.calc_grad_bce(0.001, 1), -1000)
        self.assertEqual(LogReg.calc_grad_bce(0.001, 0), 1.001001001001001)

    def test_calc_grad_sigmoid(self):
        self.assertEqual(LogReg.calc_grad_sigmoid(0), 0)
        self.assertEqual(LogReg.calc_grad_sigmoid(0.25), 0.1875)
        self.assertEqual(LogReg.calc_grad_sigmoid(0.5), 0.25)
        self.assertEqual(LogReg.calc_grad_sigmoid(0.75), 0.1875)
        self.assertEqual(LogReg.calc_grad_sigmoid(1), 0)

    def test_calc_z(self):
        self.assertEqual(self.lr.calc_z([4, 5]), 24)

    def test_calc_g(self):
        lr = LogReg()
        self.assertEqual(lr.calc_g(math.log(1)), 0.5)

    def test_calc_loss(self):
        self.assertEqual(self.lr.calc_loss(1), 3.775135759625163e-11)
        self.assertEqual(self.lr.calc_loss(0), 23.999999678084425)

    def test_calc_grad_loss(self):
        self.assertEqual(self.lr.calc_grad_loss(1), -1.0000000000377514)
        self.assertEqual(self.lr.calc_grad_loss(0), 26489113602.583836)

    def test_calc_grads(self):
        x = 4, 5
        y = 1
        self.lr.calc_grads(y, x)
        self.assertEqual(self.lr.grads[0], -3.775135759553905e-11)
        self.assertEqual(self.lr.grads[1], -1.510054303821562e-10)
        self.assertEqual(self.lr.grads[2], -1.8875678797769524e-10)
        y = 0
        self.lr.calc_grads(y, x)
        self.assertEqual(self.lr.grads[0], 0.9999999999622485)
        self.assertEqual(self.lr.grads[1], 3.999999999848994)
        self.assertEqual(self.lr.grads[2], 4.9999999998112425)

    def test_after_one_round(self):
        x = 4, 5
        y = 0
        self.assertEqual(self.lr.w[0], 1)
        self.assertEqual(self.lr.w[1], 2)
        self.assertEqual(self.lr.w[2], 3)
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x)), 0.9999999999622486)
        self.lr.calc_grads(y, x)
        self.lr.update_w(0.5)
        self.assertEqual(self.lr.w[0], 0.5000000000188758)
        self.assertEqual(self.lr.w[1], 7.550293723568302e-11)
        self.assertEqual(self.lr.w[2], 0.5000000000943787)
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x)), 0.9525741268582485)

    def test_after_2_rounds(self):
        x = 4, 5
        y = 0
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x)), 0.9999999999622486)
        for _ in range(2):
            self.lr.calc_grads(y, x)
            self.lr.update_w(0.5)
        self.assertEqual(self.lr.w[0], 3.775152412899274e-11)
        self.assertEqual(self.lr.w[1], -1.9999999998489941)
        self.assertEqual(self.lr.w[2], -1.9999999998112425)
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x)), 1.5229979536908425e-08)

    def test_after_2_rounds_slow_learner(self):
        x = 4, 5
        y = 0
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x)), 0.9999999999622486)
        for _ in range(2):
            self.lr.calc_grads(y, x)
            self.lr.update_w(0.27)
        self.assertEqual(self.lr.w[0], 0.4600000000203858)
        self.assertEqual(self.lr.w[1], -0.15999999991845693)
        self.assertEqual(self.lr.w[2], 0.30000000010192895)
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x)), 0.7891817066647028)

    def test_after_5_rounds_slow_learner(self):
        x = 4, 5
        y = 0
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x)), 0.9999999999622486)
        for _ in range(5):
            self.lr.calc_grads(y, x)
            self.lr.update_w(0.12)
        self.assertEqual(self.lr.w[0], 0.4000000000226508)
        self.assertEqual(self.lr.w[1], -0.3999999999093965)
        self.assertEqual(self.lr.w[2], 1.1325429483122207e-10)
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x)), 0.23147521667021978)

    def test_predict(self):
        x = 4, 5
        self.assertEqual(self.lr.predict(x), LogReg.sigmoid(24))



def main() -> None:
    unittest.main()

if __name__ == "__main__":
    main()



