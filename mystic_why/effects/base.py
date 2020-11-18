from mystic_why.core.light import FullLightning, PerLedLightning


class BaseEffect:
    def __init__(self, area):
        self.area = area

    def run_step(self):
        pass

    def on_exit(self):
        pass


class FullLightEffect(BaseEffect):
    light: FullLightning

    def __init__(self, area):
        super().__init__(area)
        self.light = FullLightning()


class PerLedEffect(BaseEffect):
    light: PerLedLightning

    def __init__(self, area):
        super().__init__(area)
        self.light = PerLedLightning()

    def on_exit(self):
        self.light.revert_to_full()
