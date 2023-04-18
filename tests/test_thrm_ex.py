#!/usr/bin/env python3
import unittest

from riic_simulator.facility import *
from riic_simulator.operator import *


class Test(unittest.TestCase):
    def test_thermal_ex(self):
        base = Base()
        power_plant = PowerPlant(base, level=3, location="B101")
        thrm_ex = ThermalEX()
        thrm_ex.put(power_plant)
        self.assertEqual(base.extra["drone_recover"]["value"], 115)
        self.assertEqual(thrm_ex.extra["morale_drain_redution"]["value"], 48)
