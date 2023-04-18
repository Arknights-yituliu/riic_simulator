#!/usr/bin/env python3
import unittest

from riic_simulator.facility import *
from riic_simulator.operator import *


class Test(unittest.TestCase):
    def test_electricity_243(self):
        base = Base()
        ControlCenter(base, level=5)
        PowerPlant(base, level=3, location="B103")
        PowerPlant(base, level=3, location="B203")
        PowerPlant(base, level=3, location="B303")
        TradingPost(base, level=3, location="B101")
        TradingPost(base, level=3, location="B102")
        Factory(base, level=3, location="B201")
        Factory(base, level=3, location="B202")
        Factory(base, level=3, location="B301")
        Factory(base, level=3, location="B302")
        Dormitory(base, level=5)
        Dormitory(base, level=5)
        Dormitory(base, level=5)
        Dormitory(base, level=5)
        ReceptionRoom(base, level=3)
        Workshop(base, level=3)
        Office(base, level=3)
        TrainingRoom(base, level=3)
        self.assertEqual(base.extra["electricity"]["value"], 810)
        self.assertEqual(base.extra["electricity_limit"]["value"], 810)
