class Base:
    def __init__(self):
        self.drone = 0
        self.drone_limit = 0
        self.electricity = 0
        self.electricity_limit = 0
        self.control_center = None
        self.dormitories = [None] * 4
        self.left_side = {}
        self.reception = None
        self.workshop = None
        self.office = None
        self.training = None


class Facility:
    def __init__(
        self,
        base=None,
        level=0,
        max_level=3,
        operators=[],
    ):
        self.base = base
        self.level = level
        self.max_level = max_level
        self.operators = operators


class ElectricityMixin:
    electricity_table = [10, 30, 60]

    def set_electricity(self):
        self.electricity = self.electricity_table[self.level - 1]
        self.base.electricity += self.electricity


class SpeedMixin:
    speed = 1

    def get_speed(self):
        speed = self.speed
        for o in self.operators:
            if o:
                speed += o.speed
        return speed


class ControlCenter(Facility):
    def __init__(self, base, level):
        super().__init__(
            base=base,
            level=level,
            max_level=5,
            operators=[None] * level,
        )
        self.assistant = None
        self.floor_assistants = [None] * (level - 1)
        base.control_center = self


class PowerPlant(Facility):
    electircity_table = [60, 130, 270]

    def __init__(self, base, level, location):
        super().__init__(
            base=base,
            level=level,
            operators=[None],
        )
        self.electricity = self.electircity_table[level - 1]
        base.left_side[location] = self
        base.electricity_limit += self.electricity


class TradingPost(Facility, ElectricityMixin):
    def __init__(self, base, level, location):
        super().__init__(
            base=base,
            level=level,
            operators=[None] * level,
        )
        self.limit = [6, 8, 10][level - 1]
        self.speed = 1
        base.left_side[location] = self
        self.set_electricity()


class Factory(Facility, ElectricityMixin, SpeedMixin):
    def __init__(self, base, level, location):
        super().__init__(
            base=base,
            level=level,
            operators=[None] * level,
        )
        self.capacity = [24, 36, 54][level - 1]
        base.left_side[location] = self
        self.location = location
        self.set_electricity()


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
