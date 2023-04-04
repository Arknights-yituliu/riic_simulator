#!/usr/bin/env python3

from riic_simulator.base import Base
from riic_simulator.facility import *
from riic_simulator.operator import *

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

B201 = base.left_side["B201"]
Mayer().put(B201)
Dorothy().put(B201)
Ptilopsis().put(B201)
print(B201.extra)


B102 = base.left_side["B102"]
Jaye().put(B102)
Lappland().put(B102)
Texas().put(B102)
print(B102.extra)

for i in range(8):
    B102.new_order()
    print(B102.extra)

B101 = base.left_side["B101"]
control_center = base.control_center
TerraResearchCommission().put(B101)
KirinXYato().put(control_center)
RathalosSNoirCorne().put(control_center)
print(base.extra)
print(B101.extra)
