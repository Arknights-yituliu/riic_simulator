#!/usr/bin/env python3
import unittest

from riic_simulator.facility import *
from riic_simulator.operator import *


class Test(unittest.TestCase):
    def test_drone_recover(self):
        base = Base()
        ControlCenter(base, level=5)
        power_plant = PowerPlant(base, level=3, location="B101")
        print(base.extra["drone_recover"])
        for i in base.extra["drone_recover"]["items"]:
            print(i.drone_recover)
        self.assertEqual(base.extra["drone_recover"]["value"], 100)
        golden_glow = GoldenGlow()
        golden_glow.put(power_plant)
        self.assertEqual(base.extra["drone_recover"]["value"], 125)
        golden_glow.remove()
        self.assertEqual(base.extra["drone_recover"]["value"], 100)
