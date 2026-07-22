from itertools import chain
from typing import Any, Optional, TYPE_CHECKING

import yaml

from Alice.core.event import AliceEvent
from Alice.core.plugin.models import PluginMetadata
from Alice.core.plugin.plugin import Plugin
from Alice.core.plugin.trigger import TriggerGroup
from Alice.core.plugin.worker import Worker
from Alice.log import logger

if TYPE_CHECKING:
    from Alice.core import AliceCore
    from Alice.core.plugin.trigger import Trigger


class PluginManager:
    '''# 插件管理器'''
    __slots__ = ('_core', '_detected', '_loaded', '_unloaded', '_workers', '_cached_trigger_group', 'current_loading_plugin')
    
    _core: AliceCore
    _detected: dict[str, Plugin]
    _loaded: dict[str, Plugin]
    _unloaded: dict[str, Plugin]
    _workers: dict[int, Worker]
    _cached_trigger_group: TriggerGroup
    current_loading_plugin: Optional[Plugin]
    '''## 当前正在被导入的插件'''
    
    def __init__(self, core: AliceCore) -> None:
        self._core = core
        self._detected = dict()
        self._loaded = dict()
        self._unloaded = dict()
        self._workers = dict()
        self._cached_trigger_group = TriggerGroup()
        self.current_loading_plugin = None
    
    def _build_cached_trigger_group(self) -> None:
        block: list[Trigger] = list()
        ordinal: list[Trigger] = list()
        triggers = list(chain(*(plugin.triggers.values() for plugin in self.loaded.values())))
        for trigger in triggers:
            if trigger.block:
                block.append(trigger)
            else:
                ordinal.append(trigger)
        block.sort(key=lambda t: t.priority)
        ordinal.sort(key=lambda t: t.priority)
        self._cached_trigger_group = TriggerGroup(block, ordinal)
    
    def _append_worker(self, worker: Worker) -> None:
        self._workers.setdefault(worker.ident, worker)
    
    def _remove_worker(self, worker: Worker) -> None:
        self._workers.pop(worker.ident, None)
    
    @property
    def detected(self) -> dict[str, Plugin]:
        return self._detected.copy()
    
    @property
    def loaded(self) -> dict[str, Plugin]:
        return self._loaded.copy()
    
    @property
    def unloaded(self) -> dict[str, Plugin]:
        return self._unloaded.copy()
    
    @property
    def workers(self) -> list[Worker]:
        return list(self._workers.values())
    
    @property
    def cached_trigger_group(self) -> TriggerGroup:
        return self._cached_trigger_group
    
    def load_all(self) -> None:
        '''## 导入所有未导入的插件'''
        for plugin in self.detected.values():
            plugin.load()
    
    def unload_all(self) -> None:
        '''## 卸载所有已导入的插件'''
        for plugin in self.detected.values():
            plugin.unload()
    
    def reload_all(self):
        for plugin in self.detected.values():
            plugin.unload()
        for plugin in self.detected.values():
            plugin.load()
    
    def detect(self) -> None:
        '''## 检测插件目录下的所有插件'''
        for path in self._core.path.plugin.iterdir():
            if not path.is_dir():
                continue
            if not (path / '__init__.py').exists():
                continue
            if not (path / 'plugin.yaml').exists():
                continue
            plugin = Plugin(path)
            try:
                with open(path / 'plugin.yaml', 'rb') as f:
                    data: dict[str, Any] = yaml.safe_load(f) or dict()
                plugin.metadata = PluginMetadata(**data)
            except:
                logger.error(f'插件[{path}]元数据加载失败.')
                continue
            logger.info(f'检测到插件[{plugin.metadata.name}][{plugin.metadata.id}]')
            sid = plugin.metadata.id
            if sid not in self._detected:
                self._detected[sid] = plugin
            if sid not in self._loaded and sid not in self._unloaded:
                self._unloaded[sid] = plugin
    
    def set_workers(self, n: int) -> None:
        '''
        ## 设置工作者数量
        
        ---
        ### 参数
        * n: 工作者数量
        '''
        assert n >= 0
        
        c = len(self.workers)
        if n > c:
            from Alice.core.thread.worker import WorkerThread
            
            exist_idents = set(self._workers.keys())
            max_ident = max(len(exist_idents), max(exist_idents)) if exist_idents else 1
            build_idents = {i for i in range(1, max_ident + (n - c) + 1)}
            idents = list(build_idents - exist_idents)[:n - c]
            for ident in idents:
                WorkerThread(ident).start()
        elif c > n:
            workers = sorted(self.workers, key=lambda w: w.actives)[c - n:]
            for worker in workers:
                worker.close()
    
    def dispatch_event(self, event: AliceEvent) -> None:
        '''
        ## 分发事件
        
        ---
        !!! 谨慎使用, 避免造成无尽递归 !!!
        
        ---
        ### 参数
        * event: 待分发事件
        '''
        if not self._workers:
            return
        min(self.workers, key=lambda w: (w.load, w.actives))(event, self._cached_trigger_group)


__all__ = [
 'PluginManager',   
]