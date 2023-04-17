
#!/usr/bin/env python3
import unittest

from riic_simulator.facility import *
from riic_simulator.operator import *


class Test(unittest.TestCase):
    def test_kaltit(self):
        base = Base()
        factory = Factory(base, level=3, location="B101")
        control_center = ControlCenter(base, level=5)
        kaltsit = Kaltsit()
        kaltsit.put(control_center)
        self.assertEqual(factory.extra["efficiency"]["value"], 2)
        kaltsit.remove()
        self.assertEqual(factory.extra["efficiency"]["value"], 0)
