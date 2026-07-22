from contextvars import Context
from typing import Optional, TYPE_CHECKING

from Alice.core.thread.thread import AliceThread

if TYPE_CHECKING:
    from Alice.core.plugin.worker import Worker


class WorkerThread(AliceThread):
    
    worker: Worker
    
    def __init__(self, ident: int, *, daemon: Optional[bool] = None, context: Optional[Context] = None) -> None:
        super().__init__(f'Worker#{ident:02d}', daemon=daemon, context=context)
        from Alice.core.plugin.worker import Worker
        
        self.worker = Worker(ident, self._core)
    
    def start(self) -> None:
        self.worker.start()
        super().start()
    
    def close(self, timeout: Optional[float] = None, block: bool = True) -> None:
        self.worker.close()
        super().close(timeout, block)
    
    async def main(self) -> None:
        await self.worker.loop()


__all__ = [
    'WorkerThread',
]