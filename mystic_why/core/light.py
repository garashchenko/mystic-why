from typing import List

import hid

import mystic_why.common.const as const
from mystic_why.common.enums import LightArea
from mystic_why.common.exception import DeviceNotFound, AreaNotFound


class Color:
    @staticmethod
    def create_by_hex(hex_value):
        hex_value = hex_value.lstrip('#')
        return Color(*tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4)))

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


class Led:
    def __init__(self, index: int, color: Color):
        self.index = index
        self.color = color


class BaseLightning:

    def __init__(self):
        self.device = hid.device()
        self.open_device()

    def get_current_state(self):
        return self.device.get_feature_report(const.HID_STATE_REPORT_ID, const.HID_STATE_REPORT_LEN)

    def open_device(self):
        try:
            device_info = next(d for d in hid.enumerate() if d['product_string'] == const.MSI_PRODUCT_STRING)
        except StopIteration:
            raise DeviceNotFound

        self.device.open(device_info['vendor_id'], device_info['product_id'])


class FullLightning(BaseLightning):

    def __init__(self):
        super().__init__()
        self.msg = []

    def fill_color_for_area(self, area, color: Color):
        if area == LightArea.JONBOARD:
            color_bytes = [const.FULL_LIGHT_ONBOARD]
        elif area == LightArea.JRAINBOW1:
            color_bytes = [const.FULL_LIGHT_JRAINBOW1]
        elif area == LightArea.JRAINBOW2:
            color_bytes = [const.FULL_LIGHT_JRAINBOW2]
        else:
            color_bytes = [const.FULL_LIGHT_ONBOARD, const.FULL_LIGHT_JRAINBOW1, const.FULL_LIGHT_JRAINBOW2]

        for color_byte in color_bytes:
            self.msg[color_byte] = color.red
            self.msg[color_byte + 1] = color.green
            self.msg[color_byte + 2] = color.blue

    def set_full_light(self, color: Color, area='ALL'):
        self.msg = self.get_current_state()
        self.fill_color_for_area(area, color)
        self.device.send_feature_report(self.msg)


class PerLedLightning(BaseLightning):
    def __init__(self, enable=True):
        super().__init__()
        self.current_state = self.get_current_state()
        if enable:
            self.enable_per_led()

    def enable_per_led(self):
        self.device.send_feature_report(const.ENABLE_PER_LED_MSG)

    def revert_to_full(self):
        self.device.send_feature_report(self.current_state)

    def set_led_colors(self, feature_data: List[int], led_info: List[Led]):
        for led in led_info:
            feature_data[(led.index % (len(feature_data) // 3)) * 3] = led.color.red
            feature_data[(led.index % (len(feature_data) // 3)) * 3 + 1] = led.color.green
            feature_data[(led.index % (len(feature_data) // 3)) * 3 + 2] = led.color.blue

    def get_color_bytes_by_area(self, area, current_state: List[int]):
        area_info = {
            LightArea.JONBOARD: {'start_byte': const.FULL_LIGHT_ONBOARD, 'led_count': const.ONBOARD_LED_COUNT},
            LightArea.JRAINBOW1: {'start_byte': const.FULL_LIGHT_JRAINBOW1, 'led_count': const.JRAINBOW1_LED_COUNT},
            LightArea.JRAINBOW2: {'start_byte': const.FULL_LIGHT_JRAINBOW2, 'led_count': const.JRAINBOW2_LED_COUNT}
        }

        try:
            selected_area = area_info[area]
        except KeyError:
            raise AreaNotFound

        start_byte = selected_area['start_byte']
        led_count = selected_area['led_count']

        return [current_state[start_byte], current_state[start_byte + 1], current_state[start_byte + 2]] * led_count

    def set_led_light(self, area, led_info, background_color=None):

        if background_color is None:
            background_color = Color(0, 0, 0)

        msg_onboard = self.get_color_bytes_by_area(LightArea.JONBOARD, self.current_state)
        msg_rainbow1 = self.get_color_bytes_by_area(LightArea.JRAINBOW1, self.current_state)
        msg_rainbow2 = self.get_color_bytes_by_area(LightArea.JRAINBOW2, self.current_state)

        # TODO: not supported
        msg_corsair = [0, 0, 0] * const.CORSAIR_LED_COUNT
        empty_trail = [0] * const.EMPTY_TRAIL_LEN

        if area == LightArea.JONBOARD:
            if background_color:
                msg_onboard = [background_color.red, background_color.green,
                               background_color.blue] * const.ONBOARD_LED_COUNT
            self.set_led_colors(msg_onboard, led_info)
        elif area == LightArea.JRAINBOW1:
            if background_color:
                msg_rainbow1 = [background_color.red, background_color.green,
                                background_color.blue] * const.JRAINBOW1_LED_COUNT
            self.set_led_colors(msg_rainbow1, led_info)
        elif area == LightArea.JRAINBOW2:
            if background_color:
                msg_rainbow2 = [background_color.red, background_color.green,
                                background_color.blue] * const.JRAINBOW2_LED_COUNT
            self.set_led_colors(msg_rainbow2, led_info)
        elif area == LightArea.ALL:
            if background_color:
                msg_onboard = [background_color.red, background_color.green,
                               background_color.blue] * const.ONBOARD_LED_COUNT
                msg_rainbow1 = [background_color.red, background_color.green,
                                background_color.blue] * const.JRAINBOW1_LED_COUNT
                msg_rainbow2 = [background_color.red, background_color.green,
                                background_color.blue] * const.JRAINBOW2_LED_COUNT
            self.set_led_colors(msg_onboard, led_info)
            self.set_led_colors(msg_rainbow1, led_info)
            self.set_led_colors(msg_rainbow2, led_info)
        else:
            raise AreaNotFound

        feature_data = const.PER_LED_MSG_HEADER + msg_onboard + msg_rainbow1 + msg_rainbow2 + msg_corsair + empty_trail

        self.device.send_feature_report(feature_data)
