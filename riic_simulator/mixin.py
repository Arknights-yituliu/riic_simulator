from pydispatch import dispatcher


class SignalNameMixin:
    @staticmethod
    def short_name(name):
        return name.split(".")[-1]

    def parse(self, signal):
        if "." not in signal:
            signal = "base." + signal
        location, name = signal.split(".")
        if location == "self":
            receiver = self
        elif location == "base":
            if hasattr(self, "base"):
                receiver = self.base
            else:
                receiver = self.facility.base
        elif location == "facility":
            if hasattr(self, "facility"):
                receiver = self.facility
            else:
                receiver = self
        elif location[0] == "B" and len(location) == 4:
            if hasattr(self, "base"):
                base = self.base
            else:
                base = self.facility.base
            receiver = base.left_side[location]
        return receiver, name


class MessageMixin(SignalNameMixin):
    def sum(self, signal):
        name = self.short_name(signal)
        result = 0
        for o in self.extra[name]["items"]:
            if hasattr(o, name):
                result += getattr(o, name)
        old_value = self.extra[name]["value"]
        if old_value != result:
            self.extra[name]["value"] = result
            dispatcher.send(signal=signal)

    def register(self, signal):
        name = self.short_name(signal)
        if name in self.extra:
            return
        self.extra[name] = {"value": 0, "items": []}
        func = f"sum_{name}"
        if not hasattr(self, func):
            setattr(self, func, lambda: self.sum(signal))
        dispatcher.connect(receiver=getattr(self, func), signal=signal)

    def add_item(self, signal, obj):
        name = self.short_name(signal)
        if not name in self.extra:
            self.register(signal)
        self.extra[name]["items"].append(obj)

    def remove_item(self, signal, operator):
        name = self.short_name(signal)
        self.extra[name]["items"].remove(operator)
        dispatcher.send(signal=signal)


class SkillMixin(SignalNameMixin):
    skill_name = []

    def wrapper(self):
        attr = [self.short_name(p) for p in self.pub]
        before = [getattr(self, p) if hasattr(self, p) else None for p in attr]
        self.skill()
        after = [getattr(self, p) for p in attr]
        for i in range(len(attr)):
            if before[i] != after[i]:
                receiver, name = self.parse(self.pub[i])
                if hasattr(receiver, "base") and receiver.base == receiver:
                    dispatcher.send(signal=f"base.{name}")
                elif hasattr(receiver, "location"):
                    dispatcher.send(signal=f"{receiver.location}.{name}")
                else:
                    dispatcher.send(signal=f"{receiver.__repr__}.{name}")
