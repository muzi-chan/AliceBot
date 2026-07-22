from typing import TYPE_CHECKING, Optional

from Alice.core.thread.thread import AliceThread

if TYPE_CHECKING:
    from Alice.core import AliceCore


class ThreadManager:
    '''# 线程管理器'''
    __slots__ = ('_core', '_threads')

    _core: AliceCore
    _threads: dict[int, AliceThread]
    
    def __init__(self, core: AliceCore) -> None:
        self._core = core
        self._threads = dict()
    
    def _append_thread(self, thread: AliceThread) -> None:
        self._threads[id(thread)] = thread
    
    def _remove_thread(self, thread: AliceThread) -> None:
        tid = id(thread)
        if tid in self._threads:
            self._threads.pop(tid)

    @property
    def threads(self) -> list[AliceThread]:
        return list(self._threads.values())
    
    def close_all(self, timeout: Optional[float] = None, block: bool = False) -> None:
        for thread in self.threads:
            thread.close(timeout, block)


__all__ = [
    'ThreadManager',
]