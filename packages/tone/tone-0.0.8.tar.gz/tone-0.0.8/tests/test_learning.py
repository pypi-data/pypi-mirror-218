# coding=utf-8
import time
import json
import unittest

from test_base import BaseTestCase

from tone import utils


class TestCase(BaseTestCase):

    def test_metrics(self):
        from tone.utils.learning import metrics
        import numpy as np

        real = np.linspace(0, 10, 100)
        pred = real + np.random.randn(real.shape[0]) * 0.01
        scores = metrics(real, pred)


if __name__ == '__main__':
    TestCase.main()
