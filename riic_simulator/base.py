from riic_simulator.mixin import MessageMixin


class Base(MessageMixin):
    def __init__(self):
        self.electricity = 0
        self.electricity_limit = 0
        self.control_center = None
        self.dormitories = [None] * 4
        self.left_side = {}
        self.reception = None
        self.workshop = None
        self.office = None
        self.training = None
        self.extra = {}
