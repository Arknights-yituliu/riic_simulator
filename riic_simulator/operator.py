from riic_simulator.facility import Factory, TradingPost, ControlCenter, PowerPlant
from riic_simulator.mixin import SkillMixin, MessageMixin
from pydispatch import dispatcher


class Operator(SkillMixin, MessageMixin):
    def __repr__(self):
        if hasattr(self, "facility") and isinstance(self.facility, Factory):
            return f"{self.name}({self.efficiency})"
        return self.name

    def __init__(self):
        self.name = self.__class__.__name__
        self.extra = {}
        self.morale_drain_redution = 100
        self.morale_increase = 0
        self.add_item(f"{self.name}.morale_drain_redution", self)
        self.add_item(f"{self.name}.morale_increase", self)

    def put(self, facility, index=None):
        self.facility = facility
        if hasattr(self, "get_sub"):
            self.sub = self.get_sub()
        elif not hasattr(self, "sub"):
            self.sub = []
        if hasattr(self, "get_pub"):
            self.pub = self.get_pub()
        elif not hasattr(self, "pub"):
            self.pub = []
        if not index:
            index = facility.operators.index(None)
        facility.operators[index] = self
        for s in self.sub:
            facility, name = self.parse(s)
            if facility == facility.base:
                signal = f"base.{name}"
            else:
                signal = f"{facility.location}.{name}"
            if name != "operators":
                facility.register(signal)
            dispatcher.connect(self.wrapper, signal=signal)
        for s in self.pub:
            facility, name = self.parse(s)
            if facility == facility.base:
                signal = f"base.{name}"
            else:
                signal = f"{facility.location}.{name}"
            if name != "operators":
                facility.add_item(signal, self)
        dispatcher.send(signal=f"{self.facility.location}.operators")
        self.wrapper()

    def remove(self):
        for s in self.sub:
            facility, name = self.parse(s)
            if facility == facility.base:
                signal = f"base.{name}"
            else:
                signal = f"{facility.location}.{name}"
            dispatcher.disconnect(self.wrapper, signal=signal)
        operators = self.facility.operators
        operators[operators.index(self)] = None
        dispatcher.send(signal=f"{self.facility.location}.operators")
        for s in self.pub:
            facility, name = self.parse(s)
            if facility == facility.base:
                signal = f"base.{name}"
            else:
                signal = f"{facility.location}.{name}"
            if name != "operators":
                facility.remove_item(signal, self)
            dispatcher.send(signal=signal)
        self.facility = None


class Jaye(Operator):
    # skill_name = ["摊贩经济"]
    skill_name = ["摊贩经济", "市井之道"]
    sub = ["facility.efficiency", "facility.limit", "facility.orders"]
    pub = ["facility.efficiency", "facility.limit"]

    def skill(self):
        print("不知道有没有适合摆摊的地方......")
        print("进驻贸易站时，当前订单数与订单上限每差1笔订单，则订单获取效率+4%")
        print("进驻贸易站时，当前贸易站内其他干员提供的每10%订单获取效率使订单上限-1（订单最少为1），同时每有1笔订单就+4%订单获取效率")
        self.efficiency = 0
        self.limit = 0
        if isinstance(self.facility, TradingPost):
            order_count = len(self.facility.orders)
            order_limit = self.facility.extra["limit"]["value"]
            self.efficiency += (order_limit - order_count) * 4

            other_efficiency = 0
            for o in self.facility.operators:
                if o and o != self and hasattr(o, "efficiency"):
                    other_efficiency += o.efficiency
            decrease = int(other_efficiency / 10)
            if decrease >= order_limit:
                decrease = order_limit - 1
            self.limit -= decrease
            self.efficiency += order_count * 4


class Lappland(Operator):
    skill_name = ["醉翁之意·β"]
    sub = ["facility.operators"]
    pub = ["facility.limit"]

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
    sub = ["facility.operators"]
    pub = ["facility.efficiency"]

    def skill(self):
        print("这里需要补充物资吗？我可以帮忙。")
        print("当与拉普兰德在同一个贸易站时，心情每小时消耗+0.3，订单获取效率+65%")
        self.efficiency = 0
        if isinstance(self.facility, TradingPost):
            for o in self.facility.operators:
                if isinstance(o, Lappland):
                    self.efficiency = 65
                    break


class Mayer(Operator):
    skill_name = ["咪波·制造型"]
    pub = ["facility.efficiency"]

    def skill(self):
        print("我想要个新的工作室了！")
        print("进驻制造站时，生产力+30%")
        self.efficiency = 0
        if isinstance(self.facility, Factory):
            self.efficiency = 30


class Dorothy(Operator):
    sub = ["facility.operators"]
    pub = ["facility.efficiency"]

    skill_name = ["莱茵科技·β", "源石技艺理论应用"]

    def skill(self):
        print("罗德岛上真热闹啊。")
        print("进驻制造站时，当前制造站内每个莱茵科技类技能为自身+5%的生产力")
        print("进驻制造站时，生产力+25%")
        self.efficiency = 0
        if isinstance(self.facility, Factory):
            for o in self.facility.operators:
                if o and "莱茵科技·β" in o.skill_name:
                    self.efficiency += 5
            self.efficiency += 25


class Ptilopsis(Operator):
    skill_name = ["莱茵科技·β"]
    pub = ["facility.efficiency"]

    def skill(self):
        print("这个地方就像磁盘列阵一样吗？")
        print("进驻制造站时，生产力+25%")
        self.efficiency = 0
        if isinstance(self.facility, Factory):
            self.efficiency = 25


class Mizuki(Operator):
    skill_name = ["意识协议"]

    def get_sub(self):
        return [f"{self.facility.location}.operators"]

    def get_pub(self):
        location = self.facility.location
        index = self.facility.operators.index(self)
        return [f"{location}.{index}.efficiency"]

    def skill(self):
        print("我来给大家做点好吃的放松下吧？")
        print("进驻制造站时，当前制造站内每个标准化类技能为自身+5%的生产力")
        self.efficiency = 0
        if isinstance(self.facility, Factory):
            for o in self.facility.operators:
                if o and ("标准化·α" in o.skill_name or "标准化·β" in o.skill_name):
                    self.efficiency += 5
            self.efficiency += 25


class KirinXYato(Operator):
    skill_name = ["耐力回复"]
    pub = ["木天蓼"]

    def skill(self):
        print("我希望承担更为艰巨的任务，但如果这是您的安排，我愿意去做。")
        print("进驻控制中枢时，自身心情每小时消耗+0.5，木天蓼+8")
        self.木天蓼 = 0
        if isinstance(self.facility, ControlCenter):
            self.木天蓼 = 8


class RathalosSNoirCorne(Operator):
    skill_name = ["团队合作"]
    sub = ["facility.operators"]
    pub = ["木天蓼"]

    def skill(self):
        print("小心，小心，让俺先把刀收起来。")
        print("进驻控制中枢时，控制中枢内每有1名怪物猎人小队干员，则木天蓼+2")
        self.木天蓼 = 0
        if isinstance(self.facility, ControlCenter):
            mh_team = [KirinXYato, RathalosSNoirCorne, TerraResearchCommission]
            for o in self.facility.operators:
                for oc in mh_team:
                    if isinstance(o, oc):
                        self.木天蓼 += 2
                        break


class TerraResearchCommission(Operator):
    skill_name = ["可爱的艾露猫"]
    sub = ["木天蓼"]
    pub = ["facility.efficiency", "facility.limit"]

    def skill(self):
        print("拖，拖喵......小工匠，你怎么去哪里都带着一大堆材料喵？")
        print("进驻贸易站时，订单获取效率+5%，且订单上限+2，同时每有1个木天蓼，则订单获取效率+3%")
        self.efficiency = 0
        self.limit = 0
        if isinstance(self.facility, TradingPost):
            self.efficiency += 5
            self.limit += 2
            base = self.facility.base
            count = base.extra["木天蓼"]["value"]
            self.efficiency += 3 * count


class Sora(Operator):
    skill_name = ["企鹅物流·β"]
    pub = ["facility.efficiency"]

    def skill(self):
        print("这里比企鹅物流的宿舍要大上好多呢！")
        print("进驻贸易站时，订单获取效率+30%")
        self.efficiency = 0
        if isinstance(self.facility, TradingPost):
            self.efficiency = 30


class Kaltsit(Operator):
    skill_name = ["最高权限"]

    def get_pub(self):
        result = []
        for i in (left_side := self.facility.base.left_side):
            if isinstance(left_side[i], Factory):
                result.append(left_side[i].location + ".efficiency")
        return result

    def skill(self):
        print("这里的基础设施完成得怎么样了？")
        print("进驻控制中枢时，所有制造站生产力+2%（同种效果取最高）")
        self.efficiency = 2


class GoldenGlow(Operator):
    skill_name = ["电荷释放 "]
    pub = ["base.drone_recover"]

    def skill(self):
        print("得离电器远一点......")
        print("进驻发电站时，无人机充能速度+20%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 20


class Liskarm(Operator):
    skill_name = ["脉冲电弧·β"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("这房间会漏电吗？有没有做好保护措施？")
        print("进驻发电站时，无人机充能速度+20%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 20


class LavaThePurgatory(Operator):
    skill_name = ["热能充能·γ"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("我还有许多事要做，就让我待在这里吧。")
        print("进驻发电站时，无人机充能速度+20%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 20


class Greyy(Operator):
    skill_name = ["静电场"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("今天要做什么呢？")
        print("进驻发电站时，无人机充能速度+20%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 20


class Ifrit(Operator):
    skill_name = ["高热充能"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("这里是什么地方啊？")
        print("进驻发电站时，无人机充能速度+15%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 15


class Passenger(Operator):
    skill_name = ["聚能"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("令人着迷的舰船，博士，萨尔贡可从未给予我这样的待遇。")
        print("进驻发电站时，无人机充能速度+15%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 15


class Glaucus(Operator):
    skill_name = ["电磁充能·β"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("没问题，但先等我找到那颗螺丝钉......")
        print("进驻发电站时，无人机充能速度+15%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 15


class Indigo(Operator):
    skill_name = ["灯塔供能模块"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("没关系，我一个人待着也可以。")
        print("进驻发电站时，无人机充能速度+15%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 15


class Pudding(Operator):
    skill_name = ["设备维护"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("呼，把小抱枕放在哪里好呢......")
        print("进驻发电站时，无人机充能速度+15%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 15


class Shaw(Operator):
    skill_name = ["设备维护"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("以后我就住这儿了对吧。")
        print("进驻发电站时，无人机充能速度+15%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 15


class Purestream(Operator):
    skill_name = ["设备维护"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("希望能有大大的浴池呀~")
        print("进驻发电站时，无人机充能速度+15%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 15


class Lava(Operator):
    skill_name = ["热能充能·α"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("好了够了，我喜欢一个人待着。")
        print("进驻发电站时，无人机充能速度+10%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 10


class Blaze(Operator):
    skill_name = ["热能充能·α"]
    pub = ["base.drone_recover"]

    def skill(self):
        print("这次罗德岛有没有添置什么新设施啊？")
        print("进驻发电站时，无人机充能速度+10%")
        self.drone_recover = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 10


class ThermalEX(Operator):
    skill_name = ["备用能源", "热情澎湃"]
    pub = ["base.drone_recover", "self.morale_drain_redution"]

    def skill(self):
        print("休息吗？哈哈对我来说还早着呢！我刚更换新的储能装置，离今天的工作结束还有50小时呢！")
        print("进驻发电站时，无人机充能速度+10%，心情每小时消耗-0.52")
        self.drone_recover = 0
        self.morale_drain_redution = 100
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 10
            self.morale_drain_redution -= 52


class Castle3(Operator):
    skill_name = ["备用能源", "作战指导录像"]
    pub = ["base.drone_recover", "facility.efficiency"]

    def skill(self):
        print("有什么Castle-3能够帮忙的吗？")
        print("进驻发电站时，无人机充能速度+10%；进驻制造站时，作战记录类配方的生产力+30%")
        self.drone_recover = 0
        self.efficiency = 0
        if isinstance(self.facility, PowerPlant):
            self.drone_recover = 10
        elif isinstance(self.facility, Factory):
            self.efficiency = 30
