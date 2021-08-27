import time
from typing import List

from mystic_why.effects.base import FullLightEffect
from mystic_why.core.light import Color
from mystic_why.effects.utils import interpolate_color


class HueWheelEffect(FullLightEffect):
    def __init__(self, color_list: List[Color], interpolation_steps: int = 50, speed: int = 300, area: str = 'ALL'):
        super().__init__(area)
        self.color_list = color_list
        self.speed = int(speed)
        self.interpolation_steps = int(interpolation_steps)
        self.current_color_index = 0
        self.area = area

    def get_current_color(self) -> Color:
        return self.color_list[self.current_color_index]

    def get_next_color_index(self):
        return (self.current_color_index + 1) % len(self.color_list)

    def get_next_color(self) -> Color:
        return self.color_list[self.get_next_color_index()]

    def run_step(self):
        current_color = self.get_current_color()
        next_color = self.get_next_color()

        for i in range(self.interpolation_steps):
            transition_color = interpolate_color(current_color, next_color, i / self.interpolation_steps)
            self.light.set_full_light(transition_color, area=self.area)
            time.sleep(self.speed / 1000)

        self.current_color_index = self.get_next_color_index()
