from math import ceil

import mystic_why.effects

import importlib
import inspect
import pkgutil
import sys

from mystic_why.core.light import Color


def get_pyinstaller_modules():
    result = []
    toc = set()
    for importer in pkgutil.iter_importers(mystic_why.__name__):
        if hasattr(importer, 'toc'):
            toc |= importer.toc
    for name in toc:
        if name.startswith(mystic_why.effects.__name__ + '.'):
            name_parts = name.split('.')
            result.append(name_parts[-1])

    return result


def get_modules():
    return [module.name for module in pkgutil.iter_modules(mystic_why.effects.__path__)]


def get_effects_list():
    result = {}
    module_names = get_modules()
    module_names.extend(get_pyinstaller_modules())
    for module_name in module_names:
        if module_name == 'base':
            continue
        effect_module = f'mystic_why.effects.{module_name}'
        importlib.import_module(effect_module)
        for name, effect_class in inspect.getmembers(sys.modules[effect_module], inspect.isclass):
            if effect_class.__module__ != effect_module:
                continue
            result[name] = effect_class
    return result


def get_effect_params(effect_class):
    result = {}
    signature = inspect.signature(effect_class.__init__)
    for parameter in signature.parameters:
        result[parameter] = signature.parameters[parameter]
    return result


def interpolate(value_from: int, value_to: int, fraction: float) -> int:
    return ceil((value_to - value_from) * fraction + value_from)


def interpolate_color(from_color: Color, to_color: Color, fraction: float) -> Color:
    return Color(red=interpolate(from_color.red, to_color.red, fraction),
                 green=interpolate(from_color.green, to_color.green, fraction),
                 blue=interpolate(from_color.blue, to_color.blue, fraction))
