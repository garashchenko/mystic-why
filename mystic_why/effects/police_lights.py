import time

from mystic_why.effects.base import FullLightEffect
from mystic_why.core.light import Color


class PoliceLightsEffect(FullLightEffect):
    def __init__(self, area, speed: int = 300):
        super().__init__(area)
        self.area = area
        self.speed = int(speed)

    def run_step(self):
        self.light.set_full_light(Color(255, 0, 0), area=self.area)
        time.sleep(self.speed / 1000)
        self.light.set_full_light(Color(0, 0, 255), area=self.area)
        time.sleep(self.speed / 1000)
