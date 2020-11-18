import time
from math import ceil
from typing import List

from mystic_why.effects.base import FullLightEffect
from mystic_why.core.light import Color


class HueWheelEffect(FullLightEffect):
    def __init__(self, color_list: List[Color], speed: int = 300, area: str = 'ALL'):
        super().__init__(area)
        self.color_list = color_list
        self.speed = int(speed)
        self.current_color_index = 0
        self.area = area

    def get_current_color(self) -> Color:
        return self.color_list[self.current_color_index]

    def get_next_color_index(self):
        return (self.current_color_index + 1) % len(self.color_list)

    def get_next_color(self) -> Color:
        return self.color_list[self.get_next_color_index()]

    @staticmethod
    def interpolate(value_from: int, value_to: int, fraction: float) -> int:
        return ceil((value_to - value_from) * fraction + value_from)

    def interpolate_color(self, from_color: Color, to_color: Color, fraction: float) -> Color:
        return Color(red=self.interpolate(from_color.red, to_color.red, fraction),
                     green=self.interpolate(from_color.green, to_color.green, fraction),
                     blue=self.interpolate(from_color.blue, to_color.blue, fraction))

    def run_step(self):
        current_color = self.get_current_color()
        next_color = self.get_next_color()

        for i in range(50):
            transition_color = self.interpolate_color(current_color, next_color, i / 50)
            self.light.set_full_light(transition_color, area=self.area)
            time.sleep(self.speed / 1000)

        self.current_color_index = self.get_next_color_index()
