#!/usr/bin/env python3
import unittest

from riic_simulator.facility import *
from riic_simulator.operator import *


class Test(unittest.TestCase):
    def test_base_attribute(self):
        base = Base()
        control_center = ControlCenter(base, level=5)
        trading_post = TradingPost(base, level=3, location="B101")
        cats = TerraResearchCommission()
        cats.put(trading_post)
        self.assertEqual(base.extra["木天蓼"]["value"], 0)
        self.assertEqual(trading_post.extra["efficiency"]["value"], 106)
        yato = KirinXYato()
        yato.put(control_center)
        self.assertEqual(base.extra["木天蓼"]["value"], 8)
        self.assertEqual(trading_post.extra["efficiency"]["value"], 130)
        noir_corne = RathalosSNoirCorne()
        noir_corne.put(control_center)
        self.assertEqual(base.extra["木天蓼"]["value"], 12)
        self.assertEqual(trading_post.extra["efficiency"]["value"], 142)
        yato.remove()
        self.assertEqual(base.extra["木天蓼"]["value"], 2)
        self.assertEqual(trading_post.extra["efficiency"]["value"], 112)
