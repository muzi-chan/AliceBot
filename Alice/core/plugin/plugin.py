import sys

from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Generic, Optional, TypeVar, overload

from Alice.core.event import AlicePluginLoadedEvent, AlicePluginUnLoadedEvent
from Alice.core.plugin.trigger import Trigger
from Alice.core.plugin.models import PluginMetadata, PluginConfig, PluginStatus, PluginExport
from Alice.core.plugin.utils import get_core
from Alice.core.plugin.virtual import VIRTUAL_EXPORT_PREFIX, VIRTUAL_PLUGIN_PREFIX
from Alice.core.thread.thread import AliceThread
from Alice.log import logger


PC = TypeVar('PC', bound=PluginConfig, default=PluginConfig)
PS = TypeVar('PS', bound=PluginStatus, default=PluginStatus)
_PC = TypeVar('_PC', bound=PluginConfig, default=PluginConfig)
_PS = TypeVar('_PS', bound=PluginStatus, default=PluginStatus)

class Plugin(Generic[PC, PS]):
    '''# 插件'''
    __slots__ = ('metadata', 'config', 'status', 'location', 'dependencies', 'dependent_plugins', 'triggers', '_exports', '_threads')
    
    metadata: PluginMetadata
    '''## 插件元数据'''
    config: PC
    '''## 插件配置'''
    status: PS
    '''## 插件状态'''
    location: Path
    '''## 插件所在路径'''
    dependencies: dict[str, Plugin]
    '''## 此插件依赖的插件'''
    dependent_plugins: dict[str, Plugin]
    '''## 依赖此插件的插件'''
    triggers: dict[int, Trigger]
    '''## 插件具有的触发器'''
    _exports: dict[str, PluginExport]
    _threads: dict[int, AliceThread]

    def __init__(self, location: Path) -> None:
        self.location = location
        self.config = PluginConfig() # type: ignore
        self.status = PluginStatus() # type: ignore
        self.dependencies = dict()
        self.dependent_plugins = dict()
        self.triggers = dict()
        self._exports = dict()
        self._threads = dict()
    
    def _append_thread(self, thread: AliceThread) -> None:
        if thread.plugin is None:
            return
        self._threads[id(thread)] = thread
    
    def _remove_thread(self, thread: AliceThread) -> None:
        if thread.plugin is None:
            return
        tid = id(thread)
        if tid in self._threads:
            self._threads.pop(tid)

    @property
    def exports(self) -> list[PluginExport]:
        '''## 插件具有的导出项'''
        return list(self._exports.values())
    
    @property
    def threads(self) -> list[AliceThread]:
        '''## 插件附属线程'''
        return list(self._threads.values())
    
    @overload
    def reconstruct(self, *, config: type[_PC]) -> Plugin[_PC, PS]:
        '''
        ## 重建配置模型
        
        ---
        ### 参数
        * config: 配置模型
        '''

    @overload
    def reconstruct(self, *, status: type[_PS]) -> Plugin[PC, _PS]:
        '''
        ## 重建状态模型
        
        ---
        ### 参数
        * status: 状态模型
        '''

    @overload
    def reconstruct(self, *, config: type[_PC], status: type[_PS]) -> Plugin[_PC, _PS]:
        '''
        ## 重建配置和状态模型
        
        ---
        ### 参数
        * config: 配置模型
        * status: 状态模型
        '''

    def reconstruct(self, config: Optional[type[_PC]] = None, status: Optional[type[_PS]] = None) -> Plugin[_PC, _PS]:
        if config is not None:
            self.config = config(**self.config.model_dump()) # type: ignore
        if status is not None:
            self.status = status(**self.status.model_dump()) # type: ignore
        return self # type: ignore
    
    def export(self, export: PluginExport) -> None:
        '''
        ## 设置插件导出项
        
        ---
        !!! 仅在插件导入阶段可用 !!!
        
        一个插件可有多个不同的导出项
        '''
        self._exports.setdefault(export.name, export)
    
    def load(self, _load_chain: Optional[list[Plugin]] = None) -> None:
        '''## 加载插件'''
        if self.status.loaded:
            return
        core = get_core()
        detected = core.plugin_manager.detected
        load_chain = _load_chain or list()
        if self in load_chain:
            raise
        load_chain.append(self) # type: ignore
        # 导入依赖项
        dependencies = self.metadata.dependencies or list()
        dependency_plugins: list[Plugin] = list()
        for dependency in dependencies:
            dp = detected.get(dependency.id, None)
            missing = False
            if dp is not None:
                dependency_plugins.append(dp)
                dp.load(load_chain)
                missing = not dp.status.loaded and not dependency.optional
            if missing:
                logger.error(f'插件[{self.metadata.name}][{self.metadata.id}]必须依赖[{dp}]缺失.')
                return
        # Python模块导入
        modules_bak = sys.modules
        core.plugin_manager.current_loading_plugin = self # type: ignore
        try:
            name = f'{VIRTUAL_PLUGIN_PREFIX}.{self.location.stem}'
            path = self.location.absolute()
            spec = spec_from_file_location(name, path / '__init__.py', submodule_search_locations=[str(path)])
            module = module_from_spec(spec) # type: ignore
            spec.loader.exec_module(module) # type: ignore
            setattr(module, '__plugin__', self)
            sys.modules[name] = module
        except:
            logger.error(f'插件[{self.metadata.name}][{self.metadata.id}]加载源文件失败.')
            return
        finally:
            sys.modules = modules_bak
            core.plugin_manager.current_loading_plugin = None
        # 添加虚拟模块
        for export in self._exports.values():
            name = f'{VIRTUAL_EXPORT_PREFIX}.{export.name}'
            module = module_from_spec(ModuleSpec(name, None))
            for k, v in export.items.items():
                setattr(module, k, v)
            sys.modules[name] = module_from_spec(ModuleSpec(name, None))
        # 成功导入
        sid = self.metadata.id
        for dp in dependency_plugins:
            dp.dependent_plugins[sid] = self # type: ignore
            self.dependencies[dp.metadata.id] = dp
        self.status.loaded = True
        core.plugin_manager._loaded[sid] = self # type: ignore
        core.plugin_manager._unloaded.pop(sid, None) # type: ignore
        core.plugin_manager._build_cached_trigger_group() # type: ignore
        logger.success(f'插件[{self.metadata.name}][{self.metadata.id}]加载成功.')
        core.plugin_manager.dispatch_event(AlicePluginLoadedEvent(plugin=self)) # type: ignore
    
    def unload(self) -> None:
        '''## 卸载插件'''
        if not self.status.loaded:
            return
        core = get_core()
        # 卸载依赖项
        for dp in self.dependent_plugins.values():
            dp.unload()
        # 移除虚拟模块
        for export in self._exports.values():
            sys.modules.pop(f'{VIRTUAL_EXPORT_PREFIX}.{export.name}', None)
        # 关闭附属线程
        for thread in self._threads.values():
            thread.close()
        # 成功卸载
        sid = self.metadata.id
        for dp in self.dependencies.values():
            dp.dependent_plugins.pop(sid, None)
            self.dependencies.pop(dp.metadata.id, None)
        self.status.loaded = False
        core.plugin_manager._unloaded[sid] = self # type: ignore
        core.plugin_manager._loaded.pop(sid, None) # type: ignore
        core.plugin_manager._build_cached_trigger_group() # type: ignore
        logger.success(f'插件[{self.metadata.name}][{self.metadata.id}]卸载成功.')
        core.plugin_manager.dispatch_event(AlicePluginUnLoadedEvent(plugin=self)) # type: ignore

    def reload(self) -> None:
        '''## 重载插件'''
        self.unload()
        self.load()


__all__ = [
    'Plugin',
]