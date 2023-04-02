from riic_simulator import *
from pydispatch import dispatcher


class Operator:
    skill_name = []
    speed = 0
    facility = None
    limit = 0

    def __repr__(self):
        return self.name

    def __init__(self):
        self.name = self.__class__.__name__

    def get_sub(self):
        return [f"{self.name}.put"]

    def get_pub(self):
        return []

    def put(self, facility, index=None):
        self.facility = facility
        if not index:
            index = facility.operators.index(None)
        facility.operators[index] = self
        for s in self.get_sub():
            dispatcher.connect(self.wrapper, signal=s)
        dispatcher.send(signal=f"{self.name}.put")
        dispatcher.send(signal=f"{self.facility.location}.operators")

    def remove(self):
        for s in self.get_sub():
            dispatcher.disconnect(self.wrapper, signal=s)
        operators = self.facility.operators
        operators[operators.index(self)] = None
        dispatcher.send(signal=f"{self.facility.location}.operators")
        self.facility = None

    def wrapper(self):
        self.skill()
        for p in self.get_pub():
            dispatcher.send(signal=p)


class Jaye(Operator):
    # skill_name = ["摊贩经济"]
    skill_name = ["摊贩经济", "市井之道"]

    def get_sub(self):
        location = self.facility.location
        return [
            f"{self.name}.put",
            f"{location}.orders",
            f"{location}.limit",
            f"{location}.speed",
        ]

    def get_pub(self):
        location = self.facility.location
        index = self.facility.operators.index(self)
        # return [f"{location}.{index}.speed"]
        return [f"{location}.{index}.speed", f"{location}.{index}.limit"]

    def skill(self):
        print("不知道有没有适合摆摊的地方......")
        print("进驻贸易站时，当前订单数与订单上限每差1笔订单，则订单获取效率+4%")
        print("进驻贸易站时，当前贸易站内其他干员提供的每10%订单获取效率使订单上限-1（订单最少为1），同时每有1笔订单就+4%订单获取效率")
        self.speed = 0
        self.limit = 0
        if isinstance(self.facility, TradingPost):
            order_count = len(self.facility.orders)
            order_limit = self.facility.limit
            self.speed += (order_limit - order_count) * 0.04

            other_speed = 0
            for o in self.facility.operators:
                if o and o != self:
                    other_speed += o.speed
            decrease = int(other_speed * 10)
            if decrease >= order_limit:
                decrease = order_limit - 1
            self.limit -= decrease
            self.speed += order_count * 0.04


class Lappland(Operator):
    skill_name = ["醉翁之意·β"]

    def get_sub(self):
        return [f"{self.facility.location}.operators"]

    def get_pub(self):
        location = self.facility.location
        index = self.facility.operators.index(self)
        return [f"{location}.{index}.limit"]

    def skill(self):
        print("咦？刚才一瞬间，好像看到了一个红色的影子。")
        print("当与德克萨斯在同一个贸易站时，心情每小时消耗-0.1，订单上限+4")
        self.limit = 0
        if isinstance(self.facility, TradingPost):
            for o in self.facility.operators:
                if isinstance(o, Texas):
                    self.limit = 4
                    break


class Texas(Operator):
    skill_name = ["恩怨", "默契"]

    def get_sub(self):
        return [f"{self.facility.location}.operators"]

    def get_pub(self):
        location = self.facility.location
        index = self.facility.operators.index(self)
        return [f"{location}.{index}.speed"]

    def skill(self):
        print("这里需要补充物资吗？我可以帮忙。")
        print("当与拉普兰德在同一个贸易站时，心情每小时消耗+0.3，订单获取效率+65%")
        self.speed = 0
        if isinstance(self.facility, TradingPost):
            for o in self.facility.operators:
                if isinstance(o, Lappland):
                    self.speed = 0.65
                    break


class Mayer(Operator):
    skill_name = ["咪波·制造型"]

    def get_pub(self):
        location = self.facility.location
        index = self.facility.operators.index(self)
        return [f"{location}.{index}.speed"]

    def skill(self):
        print("我想要个新的工作室了！")
        print("进驻制造站时，生产力+30%")
        self.speed = 0
        if isinstance(self.facility, Factory):
            self.speed = 0.3


class Dorothy(Operator):
    skill_name = ["莱茵科技·β", "源石技艺理论应用"]

    def get_sub(self):
        return [f"{self.facility.location}.operators"]

    def get_pub(self):
        location = self.facility.location
        index = self.facility.operators.index(self)
        return [f"{location}.{index}.speed"]

    def skill(self):
        print("罗德岛上真热闹啊。")
        print("进驻制造站时，当前制造站内每个莱茵科技类技能为自身+5%的生产力")
        print("进驻制造站时，生产力+25%")
        self.speed = 0
        if isinstance(self.facility, Factory):
            for o in self.facility.operators:
                if o and "莱茵科技·β" in o.skill_name:
                    self.speed += 0.05
            self.speed += 0.25


class Ptilopsis(Operator):
    skill_name = ["莱茵科技·β"]

    def get_pub(self):
        location = self.facility.location
        index = self.facility.operators.index(self)
        return [f"{location}.{index}.speed"]

    def skill(self):
        print("这个地方就像磁盘列阵一样吗？")
        print("进驻制造站时，生产力+25%")
        self.speed = 0
        if isinstance(self.facility, Factory):
            self.speed = 0.25


class Mizuki(Operator):
    skill_name = ["意识协议"]

    def get_sub(self):
        return [f"{self.facility.location}.operators"]

    def get_pub(self):
        location = self.facility.location
        index = self.facility.operators.index(self)
        return [f"{location}.{index}.speed"]

    def skill(self):
        print("我来给大家做点好吃的放松下吧？")
        print("进驻制造站时，当前制造站内每个标准化类技能为自身+5%的生产力")
        self.speed = 0
        if isinstance(self.facility, Factory):
            for o in self.facility.operators:
                if o and ("标准化·α" in o.skill_name or "标准化·β" in o.skill_name):
                    self.speed += 0.05
            self.speed += 0.25



class KirinXYato(Operator):
    skill_name = ["耐力回复"]

    def get_pub(self):
        return ["木天蓼"]

    def skill(self):
        print("我希望承担更为艰巨的任务，但如果这是您的安排，我愿意去做。")
        print("进驻控制中枢时，自身心情每小时消耗+0.5，木天蓼+8")
        if isinstance(self.facility, ControlCenter):
            extra = self.facility.base.extra
            extra.setdefault("木天蓼", 0)
            extra["木天蓼"] += 8


class RathalosSNoirCorne(Operator):
    skill_name = ["团队合作"]

    def get_sub(self):
        return [f"{self.facility.location}.operators"]

    def get_pub(self):
        return ["木天蓼"]

    def skill(self):
        print("小心，小心，让俺先把刀收起来。")
        print("进驻控制中枢时，控制中枢内每有1名怪物猎人小队干员，则木天蓼+2")
        if isinstance(self.facility, ControlCenter):
            mh_team = [KirinXYato, RathalosSNoirCorne, TerraResearchCommission]
            extra = self.facility.base.extra
            for o in self.facility.operators:
                for oc in mh_team:
                    if isinstance(o, oc):
                        extra.setdefault("木天蓼", 0)
                        extra["木天蓼"] += 2
                        break


class TerraResearchCommission(Operator):
    skill_name = ["可爱的艾露猫"]

    def get_sub(self):
        return [f"{self.name}.put", "木天蓼"]

    def get_pub(self):
        location = self.facility.location
        index = self.facility.operators.index(self)
        return [f"{location}.{index}.speed", f"{location}.{index}.limit"]

    def skill(self):
        print("拖，拖喵......小工匠，你怎么去哪里都带着一大堆材料喵？")
        print("进驻贸易站时，订单获取效率+5%，且订单上限+2，同时每有1个木天蓼，则订单获取效率+3%")
        self.speed = 0
        self.limit = 0
        if isinstance(self.facility, TradingPost):
            self.speed += 0.05
            self.limit += 2
            extra = self.facility.base.extra
            extra.setdefault("木天蓼", 0)
            count = extra["木天蓼"]
            self.speed += 0.03 * count
