import random
from pydispatch import dispatcher
from riic_simulator.mixin import *


class Base(MessageMixin, SkillMixin):
    pub = ["base.drone_recover"]

    def __init__(self):
        self.base = self
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


class Facility(SkillMixin):
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

    def register_events(self):
        signal = f"{self.location}.operators"
        dispatcher.connect(self.wrapper, signal=signal)
        if hasattr(self, "get_pub"):
            self.pub = self.get_pub()
        elif not hasattr(self, "pub"):
            self.pub = []
        for s in self.pub:
            receiver, name = self.parse(s)
            if isinstance(receiver, Base):
                signal = f"base.{name}"
            elif isinstance(receiver, Facility):
                signal = f"{receiver.location}.{name}"
            else:
                signal = f"{receiver.__repr__}.{name}"
            receiver.add_item(signal, self)
        self.wrapper()


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


class PowerPlant(Facility):
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
        self.register_events()

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


class TradingPost(Facility, MessageMixin):
    def get_pub(self):
        return [
            f"{self.location}.efficiency",
            f"{self.location}.orders",
            f"{self.location}.limit",
            "base.electricity",
        ]

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
        self.probability_table = {
            1: {2: 1, 3: 0, 4: 0},
            2: {2: 0.6, 3: 0.4, 4: 0},
            3: {2: 0.3, 3: 0.5, 4: 0.2},
        }[level]
        self.orders = []
        self.limit = [6, 8, 10][self.level - 1]
        self.register_events()

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
        self.electricity = [10, 30, 60][self.level - 1]


class Factory(Facility, MessageMixin):
    def get_pub(self):
        return [
            f"{self.location}.efficiency",
            f"{self.location}.limit",
            "base.electricity",
        ]

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

        self.register_events()

    def skill(self):
        print("生产力（默认值：1）每进驻1名干员即可获得1%的基础加成。")
        count = 0
        for o in self.operators:
            if o:
                count += 1
        self.efficiency = 100 + count if count > 0 else 0
        self.electricity = [10, 30, 60][self.level - 1]


class Dormitory(Facility):
    pub = ["base.electricity"]

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
        self.register_events()

    def skill(self):
        self.electricity = [10, 20, 30, 45, 65][self.level - 1]


class ReceptionRoom(Facility):
    pub = ["base.electricity"]

    def __init__(self, base, level):
        Facility.__init__(
            self,
            base=base,
            level=level,
            operators=[None],
        )
        base.reception = self
        self.register_events()

    def skill(self):
        self.electricity = [10, 30, 60][self.level - 1]


class Workshop(Facility):
    pub = ["base.electricity"]

    def __init__(self, base, level):
        Facility.__init__(
            self,
            base=base,
            level=level,
            operators=[None],
        )
        base.workshop = self
        self.register_events()

    def skill(self):
        self.electricity = 10


class Office(Facility):
    pub = ["base.electricity"]

    def __init__(self, base, level):
        Facility.__init__(
            self,
            base=base,
            level=level,
            operators=[None],
        )
        base.office = self
        self.register_events()

    def skill(self):
        self.electricity = [10, 30, 60][self.level - 1]


class TrainingRoom(Facility):
    pub = ["base.electricity"]

    def __init__(self, base, level):
        Facility.__init__(
            self,
            base=base,
            level=level,
            operators=[None],
        )
        base.training = self
        self.register_events()

    def skill(self):
        self.electricity = [10, 30, 60][self.level - 1]
