from contextvars import Context
from threading import Thread as _Thread
from typing import Optional, TYPE_CHECKING

from Alice.log import logger

if TYPE_CHECKING:
    from Alice.core.core import AliceCore
    from Alice.core.plugin import Plugin


class AliceThread(_Thread):
    '''
    # Alice统一线程类
    
    ---
    一般情况下, 应重写 `main()` 而不是原先的 `run()`
    ```
    class CustomThread(AliceThread):
        
        async def main(self) -> None:
            pass
    ```
    '''
    _context: Context
    _core: AliceCore
    _plugin: Optional[Plugin]
    _loop_running: bool

    def __init__(self, name: Optional[str] = None, plugin: Optional[Plugin] = None, *, daemon: Optional[bool] = None, context: Optional[Context] = None) -> None:
        if plugin is None:
            perfix = 'Alice|'
        else:
            perfix = f'Plugin|{plugin.metadata.name}|'
        name = perfix + (name or str(id(self)))
        super().__init__(name=name, daemon=daemon, context=context) # type: ignore
        from Alice.plugin import get_core

        self._core = get_core()
        self._plugin = plugin
        self._loop_running = False
    
    def _register(self) -> None:
        self._core.thread_mamager._append_thread(self) # type: ignore
        if self.plugin is not None:
            self.plugin._append_thread(self) # type: ignore
    
    def _unregister(self) -> None:
        self._core.thread_mamager._remove_thread(self) # type: ignore
        if self.plugin is not None and self in self.plugin.threads:
            self.plugin._remove_thread(self) # type: ignore

    async def _main(self) -> None:
        logger.info('启动.')
        try:
            self._loop_running = True
            await self.main()
        except:
            logger.error('异常退出.')
        else:
            logger.info('退出.')
        finally:
            self._loop_running = False
            self._unregister()
    
    @property
    def plugin(self) -> Optional[Plugin]:
        '''## 所属插件'''
        return self._plugin
    
    def run(self) -> None:
        from Alice.lib.loop import run
        run(self._main())
    
    def start(self) -> None:
        self._register()
        super().start()
    
    def close(self, timeout: Optional[float] = None, block: bool = True) -> None:
        if block:
            self.join(timeout)
        else:
           _Thread(target=self.join, kwargs={'timeout': timeout}).start()
        self._unregister()
        
    def copy(self) -> AliceThread:
        return AliceThread(name=self.name, daemon=self.daemon, context=self._context)

    async def main(self) -> None:
        pass


__all__ = [
    'AliceThread',
]