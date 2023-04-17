import random
from pydispatch import dispatcher
from riic_simulator.mixin import *


class Base(MessageMixin, SkillMixin):
    pub = ["base.drone_recover"]

    def __init__(self):
        self.base = self
        self.electricity = 0
        self.control_center = None
        self.dormitories = [None] * 4
        self.left_side = {}
        self.reception = None
        self.workshop = None
        self.office = None
        self.training = None
        self.extra = {}

        for i in self.pub:
            self.add_item(i, self)
        self.wrapper()

    def skill(self):
        self.drone_recover = 100


class Facility:
    def __init__(
        self,
        base=None,
        level=0,
        max_level=3,
        location="",
        operators=[],
    ):
        self.base = base
        self.level = level
        self.max_level = max_level
        self.location = location
        self.operators = operators
        self.extra = {}


class ElectricityMixin:
    electricity_table = [10, 30, 60]

    def set_electricity(self):
        self.electricity = self.electricity_table[self.level - 1]
        self.base.electricity += self.electricity


class ControlCenter(Facility):
    def __init__(self, base, level):
        super().__init__(
            base=base,
            level=level,
            max_level=5,
            location="control_center",
            operators=[None] * level,
        )
        self.assistant = None
        self.floor_assistants = [None] * (level - 1)
        base.control_center = self


class PowerPlant(Facility, SkillMixin):
    electircity_table = [60, 130, 270]
    pub = ["base.electricity_limit", "base.drone_recover"]

    def __init__(self, base, level, location):
        super().__init__(
            base=base,
            level=level,
            location=location,
            operators=[None],
        )
        base.left_side[location] = self
        for i in self.pub:
            self.base.add_item(i, self)
        self.wrapper()

    def skill(self):
        self.electricity_limit = self.electircity_table[self.level - 1]
        self.drone_recover = 0
        if self.operators[0]:
            self.drone_recover = 5


class PureGoldOrder:
    time_table = {2: 144, 3: 210, 4: 276}
    lmd_per_gold = 500

    def __repr__(self):
        return f"{self.count}赤金订单"

    def __init__(self, probability_table):
        self.count = random.choices(
            list(probability_table.keys()),
            weights=probability_table.values(),
            k=1,
        )[0]
        self.total_time = self.time_table[self.count]
        self.time = 0
        self.lmd = self.lmd_per_gold * self.count


class TradingPost(Facility, ElectricityMixin, MessageMixin, SkillMixin):
    pub = ["facility.efficiency", "facility.orders", "facility.limit"]

    def __repr__(self):
        return f"{self.__class__.__name__}@{self.location}"

    def __init__(self, base, level, location):
        super().__init__(
            base=base,
            level=level,
            location=location,
            operators=[None] * level,
        )
        base.left_side[location] = self
        self.set_electricity()
        self.probability_table = {
            1: {2: 1, 3: 0, 4: 0},
            2: {2: 0.6, 3: 0.4, 4: 0},
            3: {2: 0.3, 3: 0.5, 4: 0.2},
        }[level]
        self.orders = []
        self.limit = [6, 8, 10][self.level - 1]

        signal = f"{self.location}.operators"
        dispatcher.connect(self.wrapper, signal=signal)
        self.add_item(f"{self.location}.efficiency", self)
        self.add_item(f"{self.location}.limit", self)
        dispatcher.send(signal=signal)

    def new_order(self):
        self.orders.append(PureGoldOrder(self.probability_table))
        dispatcher.send(signal=f"{self.location}.orders")

    def sum_orders(self):
        pass

    def skill(self):
        print("获取订单效率（默认值：1），每进驻1名干员即可获得1%的基础加成。")
        count = 0
        for o in self.operators:
            if o:
                count += 1
        self.efficiency = 100 + count if count > 0 else 0


class Factory(Facility, ElectricityMixin, MessageMixin, SkillMixin):
    pub = ["facility.efficiency", "facility.limit"]

    def __repr__(self):
        return f"{self.__class__.__name__}@{self.location}"

    def __init__(self, base, level, location):
        super().__init__(
            base=base,
            level=level,
            location=location,
            operators=[None] * level,
        )
        self.limit = [24, 36, 54][level - 1]
        base.left_side[location] = self
        self.set_electricity()

        signal = f"{self.location}.operators"
        dispatcher.connect(self.wrapper, signal=signal)
        self.add_item(f"{self.location}.efficiency", self)
        dispatcher.send(signal=signal)

    def skill(self):
        print("生产力（默认值：1）每进驻1名干员即可获得1%的基础加成。")
        count = 0
        for o in self.operators:
            if o:
                count += 1
        self.efficiency = 100 + count if count > 0 else 0


class Dormitory(Facility, ElectricityMixin):
    electricity_table = [10, 20, 30, 45, 65]

    def __init__(self, base, level, index=None):
        super().__init__(
            base=base,
            level=level,
            max_level=5,
            operators=[None] * 5,
        )
        self.ambience = 0
        self.ambience_limit = 1000 * level
        if not index:
            index = base.dormitories.index(None)
        base.dormitories[index] = self
        self.set_electricity()


class ReceptionRoom(Facility, ElectricityMixin):
    def __init__(self, base, level):
        Facility.__init__(
            self,
            base=base,
            level=level,
            operators=[None],
        )
        base.reception = self
        self.set_electricity()


class Workshop(Facility, ElectricityMixin):
    electricity_table = [10, 10, 10]

    def __init__(self, base, level):
        Facility.__init__(
            self,
            base=base,
            level=level,
            operators=[None],
        )
        base.workshop = self
        self.set_electricity()


class Office(Facility, ElectricityMixin):
    def __init__(self, base, level):
        Facility.__init__(
            self,
            base=base,
            level=level,
            operators=[None],
        )
        base.office = self
        self.set_electricity()


class TrainingRoom(Facility, ElectricityMixin):
    def __init__(self, base, level):
        Facility.__init__(
            self,
            base=base,
            level=level,
            operators=[None],
        )
        base.training = self
        self.set_electricity()
