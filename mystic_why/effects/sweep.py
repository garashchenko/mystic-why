import time

from mystic_why.effects.base import PerLedEffect
from mystic_why.core.light import Color, Led


class SweepEffect(PerLedEffect):
    def __init__(self, area, background_color: Color, sweep_color: Color, led_count: int = 12, speed: int = 300):
        super().__init__(area)
        self.speed = int(speed)
        self.current_step = 0
        self.led_count = int(led_count)
        self.background_color = background_color
        self.sweep_color = sweep_color
        self.area = area

    def run_step(self):
        led_info = [Led(index=self.current_step, color=self.sweep_color)]
        self.light.set_led_light(self.area, led_info, background_color=self.background_color)
        self.current_step = (self.current_step + 1) % self.led_count
        time.sleep(self.speed / 1000)
