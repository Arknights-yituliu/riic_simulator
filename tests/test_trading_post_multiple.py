#!/usr/bin/env python3
import unittest

from riic_simulator.facility import *
from riic_simulator.operator import *


class Test(unittest.TestCase):
    def test_trading_post_multiple(self):
        base = Base()
        trading_post = TradingPost(base, level=3, location="B101")
        jaye = Jaye()
        lappy = Lappland()
        texas = Texas()
        jaye.put(trading_post)
        self.assertEqual(trading_post.extra["efficiency"]["value"], 141)
        lappy.put(trading_post)
        self.assertEqual(trading_post.extra["efficiency"]["value"], 142)
        texas.put(trading_post)
        self.assertEqual(trading_post.extra["efficiency"]["value"], 200)
        lappy.remove()
        self.assertEqual(trading_post.extra["efficiency"]["value"], 142)
        jaye.remove()
        texas.remove()
