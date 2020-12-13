import json
import threading
import time
from typing import List

import PySimpleGUIQt as sg

from mystic_why.common import enums
from mystic_why.common.const import SETTINGS_FILE
from mystic_why.core.light import Color
from mystic_why.effects.utils import get_effects_list, get_effect_params


class EventLoopTerminated(BaseException):
    pass


class AppGui:
    layout = []
    window = None
    tray = None
    current_area = ''
    current_effect = ''
    effect_params = {}
    effect_thread = None
    exit_on_stopped = False
    has_defaults = False

    def __init__(self, areas=None, effects=None):
        if areas is None:
            self.areas = [area.value for area in enums.LightArea]
        if effects is None:
            self.effects = get_effects_list()
        self.create_system_tray()
        self.build_base_window()
        self.load_defaults()

    def build_basic_layout(self):
        return [[sg.Text('RGB area:', key='AREAS_TXT')],
                [sg.Listbox(values=self.areas, size=(20, len(self.areas)), enable_events=True,
                            key='AREAS', default_values=self.current_area)],
                [sg.Text('Effect:', key='EFFECTS_TXT')],
                [sg.Listbox(values=list(self.effects.keys()), key='EFFECTS',
                            size=(20, len(self.areas)), enable_events=True, default_values=self.current_effect)]]

    def build_base_window(self):
        self.layout = self.build_basic_layout()
        self.window = sg.Window('Mystic Why', self.layout)

    def build_ext_window(self):
        self.layout = self.build_basic_layout()
        for param, param_info in self.effect_params.items():
            if param in ['self', 'area']:
                continue

            if param_info.annotation is Color:
                self.layout.extend([[sg.Text(param)],
                                    [sg.Input(visible=False, enable_events=True, key=f'COLOR_{param}'),
                                     sg.ColorChooserButton('Pick a color', key=f'COLOR_{param}_btn',
                                                           target=f'COLOR_{param}')]])
            elif param_info.annotation is List[Color]:
                self.layout.extend([[sg.Text(param)]])
                for i in range(8):
                    self.layout.extend([[sg.Input(visible=False, enable_events=True, key=f'COLOR_LIST_{i}_{param}')],
                                        [sg.ColorChooserButton('Pick a color', key=f'COLOR_LIST_{i}_{param}_btn',
                                                               target=f'COLOR_LIST_{i}_{param}')]])
            else:
                self.layout.extend([[sg.Text(param)],
                                    [sg.InputText(key=param, default_text=param_info.default)]])

        self.layout.extend([[sg.Button('Run', key='RUN')],
                            [sg.Button('Stop', key='STOP', visible=False)],
                            [sg.Button('Save as default', key='SAVE', visible=True)],
                            [sg.Button('Load defaults', key='LOAD', visible=self.has_defaults)],
                            [sg.Text('Waiting for the effect thread to stop...', justification='center',
                                     key='STOP_TXT', visible=False),
                             sg.Input(visible=False, enable_events=True, key='THREAD_STOPPED')]])

        self.window = sg.Window('Mystic Why', self.layout, finalize=True)

    def process_effects_selected(self, event, values):
        try:
            self.current_effect = values[event][0]
            self.effect_params = get_effect_params(self.effects[self.current_effect])
            self.window.close()
            self.build_ext_window()
        except IndexError:
            return

    def process_area_selected(self, event, values):
        try:
            self.current_area = values[event][0]
        except IndexError:
            return

    def build_kwargs_from_screen(self, values):
        kwargs = {'area': self.current_area if self.current_area else enums.LightArea.ALL}
        for param, param_info in self.effect_params.items():
            if param in ['self', 'area']:
                continue

            if param_info.annotation is Color:
                kwargs[param] = Color.create_by_hex(values[f'COLOR_{param}'])
            elif param_info.annotation is List[Color]:
                kwargs[param] = []
                color_items = {k: v for k, v in values.items() if k.endswith(param)}
                for key, color in color_items.items():
                    if color:
                        kwargs[param].append(Color.create_by_hex(color))

            else:
                kwargs[param] = values[param]

        return kwargs

    def set_listbox_visibility(self, listbox_key, visible):
        self.window[listbox_key].Update(visible=visible)
        self.window[f'{listbox_key}_TXT'].Update(visible=visible)

    def run_effect_loop(self):
        thread = threading.current_thread()
        effect = getattr(thread, "effect")
        while getattr(thread, "active", True):
            effect.run_step()
        effect.on_exit()
        setattr(thread, "effect", None)

    def stop_effect_thread(self):
        self.effect_thread.active = False
        while self.effect_thread.effect:
            # waiting for thread to finish
            time.sleep(0.5)
        self.effect_thread = None
        self.window['THREAD_STOPPED'].Update(value='True')

    def process_run(self, event, values):
        if self.effect_thread:
            self.stop_effect_thread()
        kwargs = self.build_kwargs_from_screen(values)
        effect_obj = self.effects[self.current_effect](**kwargs)
        self.effect_thread = threading.Thread(target=self.run_effect_loop, daemon=True)
        self.effect_thread.active = True
        self.effect_thread.effect = effect_obj
        self.effect_thread.start()
        self.set_listbox_visibility('AREAS', visible=False)
        self.set_listbox_visibility('EFFECTS', visible=False)
        self.window['RUN'].Update(visible=False)
        self.window['STOP'].Update(visible=True)

    def process_stop(self):
        threading.Thread(target=self.stop_effect_thread, daemon=True).start()
        self.window['STOP'].Update(visible=False)
        self.window['STOP_TXT'].Update(visible=True)

    def process_save(self, values):
        with open(SETTINGS_FILE, 'w+') as outfile:
            json.dump(values, outfile)
            self.has_defaults = True
            self.window['LOAD'].update(visible=True)

    def load_defaults(self):
        try:
            with open(SETTINGS_FILE) as file:
                settings = json.load(file)
                self.has_defaults = True
                self.process_area_selected('AREAS', settings)
                self.process_effects_selected('EFFECTS', settings)
                for key, value in settings.items():
                    if key in ('AREAS', 'EFFECTS'):
                        continue
                    self.window[key].update(value=value)
                    if key.startswith('COLOR'):
                        self.window[f'{key}_btn'].update(button_color=('black', value))
        except IOError:
            self.has_defaults = False
            return

    def process_stopped(self, event, values):
        if values['THREAD_STOPPED'] == 'True':
            self.set_listbox_visibility('AREAS', visible=True)
            self.set_listbox_visibility('EFFECTS', visible=True)
            self.window['STOP_TXT'].Update(visible=False)
            self.window['RUN'].Update(visible=True)
            self.window['THREAD_STOPPED'].Update(value='False')
            if self.exit_on_stopped:
                raise EventLoopTerminated

    def create_system_tray(self):
        menu_def = ['BLANK', ['E&xit']]
        self.tray = sg.SystemTray(menu=menu_def, data_base64=sg.DEFAULT_BASE64_ICON)
        self.tray.hide()

    def check_tray_events(self):
        event = self.tray.read(timeout=100)
        if event == 'Exit':
            if self.effect_thread:
                self.exit_on_stopped = True
                self.process_stop()
                return
            raise EventLoopTerminated
        elif event == '__ACTIVATED__':
            self.tray.hide()
            if self.current_effect:
                self.build_ext_window()
            else:
                self.build_base_window()

    def check_window_events(self):
        if not self.window:
            return

        event, values = self.window.read()
        if event == sg.WIN_CLOSED:
            self.window.close()
            self.window = None
            self.tray.un_hide()
            self.tray.ShowMessage('Still running', 'Mystic Why is still running in tray')
        elif event == 'RUN':
            self.process_run(event, values)
        elif event == 'STOP':
            self.process_stop()
        elif event == 'SAVE':
            self.process_save(values)
        elif event == 'LOAD':
            self.load_defaults()
        elif event == 'THREAD_STOPPED':
            self.process_stopped(event, values)
        elif event == 'EFFECTS':
            self.process_effects_selected(event, values)
        elif event == 'AREAS':
            self.process_area_selected(event, values)
        elif event.startswith('COLOR_'):
            self.window.FindElement(f'{event}_btn').Update(button_color=('black', values[event]))

    def run_event_loop(self):
        while True:
            try:
                self.check_window_events()
                self.check_tray_events()
            except EventLoopTerminated:
                break


def show_main_window():
    gui = AppGui()
    gui.run_event_loop()
