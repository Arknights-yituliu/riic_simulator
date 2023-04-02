#!/usr/bin/env python3

from riic_simulator import *
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

Mayer().put(base.left_side["B201"])

print(base.left_side["B201"].operators)
print(base.left_side["B201"].speed)

Dorothy().put(base.left_side["B201"])

print(base.left_side["B201"].operators)
print(base.left_side["B201"].speed)

Ptilopsis().put(base.left_side["B201"])

print(base.left_side["B201"].operators)
print(base.left_side["B201"].speed)

base.left_side["B201"].operators[2].remove()

print(base.left_side["B201"].operators)
print(base.left_side["B201"].speed)

B102 = base.left_side["B102"]
Jaye().put(B102)
Lappland().put(B102)
Texas().put(B102)
for i in range(8):
    print(f"订单数：{len(B102.orders)}/{B102.limit}，效率：{B102.speed}")
    B102.new_order()
print(B102.orders)
