#!/usr/bin/env python
#
# logreg.py
# 2022-04-25

from __future__ import annotations

import math
import unittest

class LogReg:
    def __init__(self, b: float=0.2, w1: float=0.3, w2: float=0.4):
        self.b = b
        self.w1 = w1
        self.w2 = w2

    def calc_z(self, x1: float, x2: float) -> float:
        self.z = self.b + self.w1 * x1 + self.w2 * x2
        return self.z

    def sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-x))

    def calc_g(self, z: float) -> float:
        self.g = self.sigmoid(z)
        return self.g

    def bce(self, g: float, y: float) -> float:
        return -(y * math.log(g) + (1 - y) * math.log(1 - g))

    def calc_loss(self, y: float) -> float:
        self.loss = self.bce(self.g, y)
        return self.loss

    def calc_grad_loss(self, y):
        self.grad_loss = ((1 - y) / (1 - self.g)) - (y / self.g)
        return self.grad_loss

    def calc_grad_sigmoid(self, g):
        return g * (1 - g)

    def calc_grad_w1(self, x1, x2, y):
        self.grad_w1 = self.calc_grad_loss(y) * self.calc_grad_sigmoid(self.g) * x1
        return self.grad_w1

    def calc_grad_w2(self, x1, x2, y):
        self.grad_w2 = self.calc_grad_loss(y) * self.calc_grad_sigmoid(self.g) * x2
        return self.grad_w2

    def calc_grad_b(self, y):
        self.grad_b = self.calc_grad_loss(y) * self.calc_grad_sigmoid(self.g) * 1
        return self.grad_b

    def update_w1(self, learning_rate):
        self.w1 -= self.grad_w1 * learning_rate

    def update_w2(self, learning_rate):
        self.w2 -= self.grad_w2 * learning_rate

    def update_b(self, learning_rate):
        self.b -= self.grad_b * learning_rate

class TestLogReg(unittest.TestCase):
    def setUp(self):
        lr = LogReg(1, 2, 3)
        x1, x2 = 4, 5
        lr.calc_g(lr.calc_z(x1, x2))
        self.lr = lr

    def test_init_params(self):
        self.assertEqual(self.lr.b, 1)
        self.assertEqual(self.lr.w1, 2)
        self.assertEqual(self.lr.w2, 3)

    def test_calc_z(self):
        self.assertEqual(self.lr.calc_z(4, 5), 24)

    def test_sigmoid(self):
        lr = LogReg()
        self.assertEqual(lr.sigmoid(math.log(1)), 0.5)

    def test_calc_g(self):
        lr = LogReg()
        self.assertEqual(lr.calc_g(math.log(1)), 0.5)

    def test_bce(self):
        lr = LogReg()
        self.assertEqual(lr.bce(0.001, 0), 0.0010005003335835344)
        self.assertEqual(lr.bce(0.999, 0), 6.907755278982136)
        self.assertEqual(lr.bce(0.001, 1), 6.907755278982137)
        self.assertEqual(lr.bce(0.999, 1), 0.0010005003335835344)

    def test_calc_loss(self):
        self.assertEqual(self.lr.calc_loss(1), 3.775135759625163e-11)
        self.assertEqual(self.lr.calc_loss(0), 23.999999678084425)

    def test_calc_grad_loss(self):
        self.assertEqual(self.lr.calc_grad_loss(1), -1.0000000000377514)
        self.assertEqual(self.lr.calc_grad_loss(0), 26489113602.583836)

    def test_calc_grad_sigmoid(self):
        lr = LogReg()
        self.assertEqual(lr.calc_grad_sigmoid(0.5), 0.25)

    def test_calc_grad_w1(self):
        x1, x2 = 4, 5
        self.assertEqual(self.lr.calc_grad_w1(x1, x2, 1), -1.510054303821562e-10)
        self.assertEqual(self.lr.calc_grad_w1(x1, x2, 0), 3.999999999848994)

    def test_calc_grad_w2(self):
        x1, x2 = 4, 5
        self.assertEqual(self.lr.calc_grad_w2(x1, x2, 1), -1.8875678797769524e-10)
        self.assertEqual(self.lr.calc_grad_w2(x1, x2, 0), 4.9999999998112425)

    def test_calc_grad_b(self):
        self.assertEqual(self.lr.calc_grad_b(1), -3.775135759553905e-11)
        self.assertEqual(self.lr.calc_grad_b(0), 0.9999999999622485)

    def test_update_w1(self):
        x1, x2 = 4, 5
        y = 0
        self.assertEqual(self.lr.w1, 2)
        self.lr.calc_grad_w1(x1, x2, y)
        self.lr.update_w1(0.5)
        self.assertEqual(self.lr.w1,  7.550293723568302e-11)

    def test_update_w2(self):
        x1, x2 = 4, 5
        y = 0
        self.assertEqual(self.lr.w2, 3)
        self.lr.calc_grad_w2(x1, x2, y)
        self.lr.update_w2(0.5)
        self.assertEqual(self.lr.w2,  0.5000000000943787)

    def test_update_b(self):
        x1, x2 = 4, 5
        y = 0
        self.assertEqual(self.lr.b, 1)
        self.lr.calc_grad_b(y)
        self.lr.update_b(0.5)
        self.assertEqual(self.lr.b,  0.5000000000188758)

    def test_after_one_round(self):
        x1, x2 = 4, 5
        y = 0
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x1, x2)), 0.9999999999622486)
        self.lr.calc_grad_w1(x1, x2, y)
        self.lr.update_w1(0.5)
        self.lr.calc_grad_w2(x1, x2, y)
        self.lr.update_w2(0.5)
        self.lr.calc_grad_b(y)
        self.lr.update_b(0.5)
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x1, x2)), 0.9525741268582485)

    def test_after_2_rounds(self):
        x1, x2 = 4, 5
        y = 0
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x1, x2)), 0.9999999999622486)
        for _ in range(2):
            self.lr.calc_grad_w1(x1, x2, y)
            self.lr.update_w1(0.5)
            self.lr.calc_grad_w2(x1, x2, y)
            self.lr.update_w2(0.5)
            self.lr.calc_grad_b(y)
            self.lr.update_b(0.5)
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x1, x2)), 1.5229979536908425e-08)

    def test_after_2_rounds_slow_learner(self):
        x1, x2 = 4, 5
        y = 0
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x1, x2)), 0.9999999999622486)
        for _ in range(2):
            self.lr.calc_grad_w1(x1, x2, y)
            self.lr.update_w1(0.27)
            self.lr.calc_grad_w2(x1, x2, y)
            self.lr.update_w2(0.27)
            self.lr.calc_grad_b(y)
            self.lr.update_b(0.27)
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x1, x2)), 0.7891817066647028)

    def test_after_5_rounds(self):
        x1, x2 = 4, 5
        y = 0
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x1, x2)), 0.9999999999622486)
        for _ in range(5):
            self.lr.calc_grad_w1(x1, x2, y)
            self.lr.update_w1(0.5)
            self.lr.calc_grad_w2(x1, x2, y)
            self.lr.update_w2(0.5)
            self.lr.calc_grad_b(y)
            self.lr.update_b(0.5)
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x1, x2)), 6.639677225899783e-36)

    def test_after_5_rounds_slow_learner(self):
        x1, x2 = 4, 5
        y = 0
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x1, x2)), 0.9999999999622486)
        for _ in range(5):
            self.lr.calc_grad_w1(x1, x2, y)
            self.lr.update_w1(0.12)
            self.lr.calc_grad_w2(x1, x2, y)
            self.lr.update_w2(0.12)
            self.lr.calc_grad_b(y)
            self.lr.update_b(0.12)
        self.assertEqual(self.lr.calc_g(self.lr.calc_z(x1, x2)), 0.23147521667021978)



def main() -> None:
    unittest.main()

if __name__ == "__main__":
    main()



