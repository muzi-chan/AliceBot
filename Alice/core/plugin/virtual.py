import sys
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec


VIRTUAL_PLUGIN_PREFIX = 'AP'
VIRTUAL_EXPORT_PREFIX = 'AE'
VIRTUAL_PLUGIN_MODULE = module_from_spec(ModuleSpec(VIRTUAL_PLUGIN_PREFIX, None))
VIRTUAL_EXPORT_MODULE = module_from_spec(ModuleSpec(VIRTUAL_EXPORT_PREFIX, None))
sys.modules[VIRTUAL_PLUGIN_PREFIX] = VIRTUAL_PLUGIN_MODULE
sys.modules[VIRTUAL_EXPORT_PREFIX] = VIRTUAL_EXPORT_MODULE


__all__ = [
    'VIRTUAL_PLUGIN_PREFIX',
    'VIRTUAL_EXPORT_PREFIX',
    'VIRTUAL_PLUGIN_MODULE',
    'VIRTUAL_EXPORT_MODULE',
]