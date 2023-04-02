#!/usr/bin/env python3

from riic_simulator import *

base = Base()

ControlCenter(base, level=5)
PowerPlant(base, level=3, location="B103")
PowerPlant(base, level=3, location="B203")
TradingPost(base, level=2, location="B101")
TradingPost(base, level=3, location="B102")
Factory(base, level=3, location="B201")
Factory(base, level=3, location="B202")
Factory(base, level=2, location="B301")
Factory(base, level=2, location="B302")
Factory(base, level=2, location="B303")
Dormitory(base, level=2)
Dormitory(base, level=1)
Dormitory(base, level=1)
Dormitory(base, level=1)
ReceptionRoom(base, level=3)
Workshop(base, level=3)
Office(base, level=3)
TrainingRoom(base, level=3)

print(f"Electricity: {base.electricity}/{base.electricity_limit}")