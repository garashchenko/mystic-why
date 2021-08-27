import time
from typing import List

from mystic_why.effects.base import PerLedEffect
from mystic_why.core.light import Color, Led
from mystic_why.effects.utils import interpolate_color


class CustomRainbowEffect(PerLedEffect):
    def __init__(self, area, color_list: List[Color], interpolation_steps: int = 15, led_count: int = 12, speed: int = 50):
        super().__init__(area)
        self.speed = int(speed)
        self.current_step = 0
        self.led_count = int(led_count)
        self.interpolation_steps = int(interpolation_steps)
        self.color_list = []

        for i in range(len(color_list)):
            next_index = i+1 if i+1 < len(color_list) else 0
            for j in range(self.interpolation_steps):
                next_color = interpolate_color(color_list[i], color_list[next_index],
                                               fraction=j/self.interpolation_steps)
                self.color_list.append(next_color)

        self.area = area

    def run_step(self):
        led_info = [Led(index=i, color=self.color_list[(self.current_step + i) % len(self.color_list)])
                    for i in range(self.led_count)]
        self.light.set_led_light(self.area, led_info)
        self.current_step = (self.current_step + 1) % len(self.color_list)
        time.sleep(self.speed / 1000)
