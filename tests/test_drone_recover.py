#!/usr/bin/env python3
import unittest

from riic_simulator.facility import *
from riic_simulator.operator import *


class Test(unittest.TestCase):
    def test_drone_recover(self):
        base = Base()
        ControlCenter(base, level=5)
        PowerPlant(base, level=3, location="B101")
        print(base.extra["drone_recover"])
        for i in base.extra["drone_recover"]["items"]:
            print(i.drone_recover)
        self.assertEqual(base.extra["drone_recover"]["value"], 100)
