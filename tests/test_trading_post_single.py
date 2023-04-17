#!/usr/bin/env python3
import unittest

from riic_simulator.facility import *
from riic_simulator.operator import *


class Test(unittest.TestCase):
    def test_trading_post_single(self):
        base = Base()
        trading_post = TradingPost(base, level=3, location="B101")
        self.assertEqual(trading_post.extra["efficiency"]["value"], 0)
        sora = Sora()
        sora.put(trading_post)
        self.assertEqual(trading_post.extra["efficiency"]["value"], 131)
        sora.remove()
        self.assertEqual(trading_post.extra["efficiency"]["value"], 0)
