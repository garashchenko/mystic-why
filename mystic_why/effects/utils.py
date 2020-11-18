import mystic_why.effects

import importlib
import inspect
import pkgutil
import sys


def get_effects_list():
    result = {}
    for module in pkgutil.iter_modules(mystic_why.effects.__path__):
        if module.name == 'base':
            continue
        effect_module = f'mystic_why.effects.{module.name}'
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
