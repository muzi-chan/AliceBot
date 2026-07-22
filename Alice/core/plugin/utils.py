import sys

from contextvars import ContextVar
from typing import Optional, TYPE_CHECKING

from Alice.core.plugin.virtual import VIRTUAL_PLUGIN_PREFIX

if TYPE_CHECKING:
    from Alice.core import AliceCore
    from Alice.core.plugin.plugin import Plugin

if TYPE_CHECKING:
    CTX_CORE: ContextVar[AliceCore] = ContextVar('CTX_CORE')
else:
    CTX_CORE = ContextVar('CTX_CORE', default=None)


def get_core() -> AliceCore:
    '''## 获取当前Alice核心实例'''
    return CTX_CORE.get()

def current_plugin() -> Optional[Plugin]:
    '''
    ## 获取当前插件
    
    ---
    仅在插件导入阶段适用
    '''
    core = get_core()
    return core.plugin_manager.current_loading_plugin 

def get_plugin_from_frame(max_depth: int = 10) -> Optional[Plugin]:
    '''
    ## 从python帧获取插件
    
    ---
    仅在插件导入后适用
    
    ---
    ### 参数
    * max_depth: 最大帧深度
    '''
    depth = 1
    while (modulename := sys._getframemodulename(1)) and depth <= max_depth: # type: ignore
        depth += 1
        if not modulename.startswith(VIRTUAL_PLUGIN_PREFIX):
            continue
        parts = modulename.split('.')
        if len(parts) < 2:
            continue
        module = sys.modules['.'.join(parts[:2])]
        plugin = getattr(module, '__plugin__', None)
        if plugin is not None:
            return plugin


__all__ = [
    'get_core',
    'current_plugin',
    'get_plugin_from_frame',
]