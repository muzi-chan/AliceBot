from asyncio import Future, get_running_loop, sleep
from pathlib import Path
from time import time, monotonic
from typing import Any, Optional, Union, overload, TYPE_CHECKING

from Alice.config import AliceCoreConfig, RAW_DEFAULT_CONFIG
from Alice.core.bot import AliceBotManager
from Alice.core.event import AliceCoreClosingEvent, AliceCoreIntervalEvent
from Alice.core.plugin.manage import PluginManager
from Alice.core.plugin.utils import CTX_CORE
from Alice.core.plugin.virtual import VIRTUAL_PLUGIN_MODULE
from Alice.core.thread import ThreadManager
from Alice.exception import ExistAliceCore
from Alice.log import logger

if not TYPE_CHECKING:
    from threading import current_thread

    from Alice.core.bot import AliceBot
    from Alice.core.event import AliceEvent
    from Alice.core.plugin import Plugin
    from Alice.core.utils import get_subclass

    current_thread().name = 'Alice|Core'
    event_subclass = get_subclass(AliceEvent)
    for event in event_subclass:
        event.model_rebuild()


class AliceCore:
    '''# Alice核心'''
    __slots__ = ('_running', '_close_future', 'config', 'bot_manager', 'plugin_manager', 'thread_mamager')
    
    _running: bool
    _close_future: Future[None]
    config: AliceCoreConfig
    '''## 全局配置'''
    bot_manager: AliceBotManager
    '''## 机器人管理器'''
    plugin_manager: PluginManager
    '''## 插件管理器'''
    thread_mamager: ThreadManager
    '''## 线程管理器'''
    #region 固定路径
    if TYPE_CHECKING:
        from enum import Enum
        
        class path(Enum):
            '''## 固定路径'''
            bots: Path
            '''## 机器人数据目录'''
            cache: Path
            '''## 缓存目录'''
            config: Path
            '''## 配置目录'''
            data: Path
            '''## 数据目录'''
            log: Path
            '''## 日志目录'''
            plugin: Path
            '''## 插件目录'''
    else:
        class path:
            bots = Path('./data/bots')
            cache = Path('./cache')
            config = Path('./config')
            data = Path('./data')
            log = Path('./log')
            plugin = Path('./plugins')
    #endregion
    
    def __init__(self) -> None:
        current_core = CTX_CORE.get()
        if current_core is self:
            raise ExistAliceCore(f'已存在Alice核心实例[{id(self)}]')
        CTX_CORE.set(self)
        self._running = False
        self.bot_manager = AliceBotManager(self)
        self.plugin_manager = PluginManager(self)
        self.thread_mamager = ThreadManager(self)
        self.path.bots.mkdir(parents=True, exist_ok=True)
        self.path.cache.mkdir(parents=True, exist_ok=True)
        self.path.config.mkdir(parents=True, exist_ok=True)
        self.path.data.mkdir(parents=True, exist_ok=True)
        self.path.log.mkdir(parents=True, exist_ok=True)
        self.path.plugin.mkdir(parents=True, exist_ok=True)
        VIRTUAL_PLUGIN_MODULE.__path__ = [str(self.path.plugin)]
    
    async def _wait_close(self) -> None:
        loop = get_running_loop()
        self._running = True
        self._close_future = loop.create_future()
        loop.create_task(self._loop_interval())
        loop.create_task(self._loop_check_bot_update())
        await self._close_future
        self.plugin_manager.dispatch_event(AliceCoreClosingEvent())
        self._running = False
        self.thread_mamager.threads
        self.thread_mamager.close_all(5)
        self.bot_manager.save_bots()
            
    async def _loop_interval(self) -> None:
        while self._running:
            await sleep(1)
            self.plugin_manager.dispatch_event(AliceCoreIntervalEvent())
    
    async def _loop_check_bot_update(self) -> None:
        loop = get_running_loop()
        while self._running:
            await sleep(10)
            for bot in self.bot_manager.bots.values():
                if not bot.connected:
                    continue
                if time() - bot.data.last_update_time > self.config.bot.update_interval:
                    loop.create_task(bot.data.update())
    
    @property
    def running(self) -> bool:
        return self._running
    
    @overload
    def load_config(self) -> None:
        '''
        ## 加载配置
        
        ---
        默认加载`./config/Alice.yaml`如不存在则创建并结束进程
        '''

    @overload
    def load_config(self, config: AliceCoreConfig) -> None:
        '''## 加载配置'''
    
    @overload
    def load_config(self, config: Union[str, Path]) -> None:
        '''## 从配置文件加载配置'''

    def load_config(self, config: Optional[Union[str, Path, AliceCoreConfig]] = None) -> None:
        if config is None:
            config = self.path.config / 'Alice.yaml'
        if isinstance(config, (str, Path)):
            from yaml import safe_load

            config = Path(config)
            if not config.exists():
                config.write_text(RAW_DEFAULT_CONFIG)
                logger.success(f'已生成配置文件[{config}].')
                logger.warning('请修改配置文件后再次启动.')
                exit()
            with open(config, mode='rb') as f:
                data = safe_load(f)
            path = config
            config = AliceCoreConfig(**data)
            logger.success(f'已加载配置文件[{path}].')
        self.config = config
    
    def start(self) -> None:
        '''## 启动'''
        import signal
        
        from Alice.lib.loop import run
        
        last_quit_time = 0
        def handle_exit(sig: int, _: Any) -> None:
            nonlocal last_quit_time
            now = monotonic()
            if now - last_quit_time >= 3:
                last_quit_time = now
                logger.warning('[3s内]再次按下[CTRL+C]后退出.')
                return
            if not self._close_future.done():
                self.close()

        signal.signal(signal.SIGINT, handle_exit)
        signal.signal(signal.SIGTERM, handle_exit)
        self.plugin_manager.detect()
        self.bot_manager.load_bots()
        for wsc in self.config.network.websocket_servers:
            self.bot_manager.create_server(wsc)
        
        self.plugin_manager.set_workers(self.config.plugin.workers)
        self.plugin_manager.load_all()
        run(self._wait_close())
    
    def close(self) -> None:
        '''## 关闭'''
        self._close_future.set_result(None)


__all__ = [
    'AliceCore',
]