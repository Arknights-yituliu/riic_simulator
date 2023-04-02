from riic_simulator import *
from pydispatch import dispatcher


class Operator:
    skill_name = []
    speed = 0

    def __init__(self):
        self.name = self.__class__.__name__

    def get_signals(self):
        return [f"{self.name}.put"]

    def put(self, facility, index=None):
        self.facility = facility
        if not index:
            index = facility.operators.index(None)
        facility.operators[index] = self
        for s in self.get_signals():
            dispatcher.connect(self.skill, signal=s)
        dispatcher.send(signal=f"{self.name}.put")
        dispatcher.send(signal=f"{self.facility.location}.operators")


class Lappland(Operator):
    def skill(self):
        print("咦？刚才一瞬间，好像看到了一个红色的影子。")


class Texas(Operator):
    def skill(self):
        print("这里需要补充物资吗？我可以帮忙。")


class Mayer(Operator):
    skill_name = ["咪波·制造型"]

    def skill(self):
        self.speed = 0
        print("我想要个新的工作室了！")
        print("进驻制造站时，生产力+30%")
        if isinstance(self.facility, Factory):
            self.speed += 0.3


class Dorothy(Operator):
    skill_name = ["莱茵科技·β", "源石技艺理论应用"]

    def get_signals(self):
        return [f"{self.facility.location}.operators"]

    def skill(self):
        self.speed = 0
        print("罗德岛上真热闹啊。")
        print("进驻制造站时，当前制造站内每个莱茵科技类技能为自身+5%的生产力")
        print("进驻制造站时，生产力+25%")
        if isinstance(self.facility, Factory):
            for o in self.facility.operators:
                if o and "莱茵科技·β" in o.skill_name:
                    self.speed += 0.05
            self.speed += 0.25


class Ptilopsis(Operator):
    skill_name = ["莱茵科技·β"]

    def skill(self):
        self.speed = 0
        print("这个地方就像磁盘列阵一样吗？")
        print("进驻制造站时，生产力+25%")
        if isinstance(self.facility, Factory):
            self.speed += 0.25
