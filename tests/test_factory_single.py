#!/usr/bin/env python3
import unittest

from riic_simulator.facility import *
from riic_simulator.operator import *


class Test(unittest.TestCase):
    def test_factory_single(self):
        base = Base()
        factory = Factory(base, level=3, location="B101")
        self.assertEqual(factory.extra["efficiency"]["value"], 0)
        mayer = Mayer()
        mayer.put(factory)
        self.assertEqual(factory.extra["efficiency"]["value"], 131)
        mayer.remove()
        self.assertEqual(factory.extra["efficiency"]["value"], 0)
