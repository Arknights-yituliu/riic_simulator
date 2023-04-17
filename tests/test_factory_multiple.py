#!/usr/bin/env python3
import unittest

from riic_simulator.facility import *
from riic_simulator.operator import *


class Test(unittest.TestCase):
    def test_factory_multiple(self):
        base = Base()
        factory = Factory(base, level=3, location="B101")
        self.assertEqual(factory.extra["efficiency"]["value"], 0)
        dorothy = Dorothy()
        dorothy.put(factory)
        self.assertEqual(factory.extra["efficiency"]["value"], 131)
        ptilopsis = Ptilopsis()
        ptilopsis.put(factory)
        self.assertEqual(factory.extra["efficiency"]["value"], 162)
        dorothy.remove()
        self.assertEqual(factory.extra["efficiency"]["value"], 126)
        ptilopsis.remove()
