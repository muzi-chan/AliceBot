from contextvars import Context
from typing import Optional, TYPE_CHECKING

from uvicorn import Config, Server

from Alice.core.thread.thread import AliceThread

if TYPE_CHECKING:
    from Alice.core.plugin import Plugin


class ServerThread(AliceThread):
    
    server: Server
        
    def __init__(self, config: Config, name: Optional[str] = None, plugin: Optional[Plugin] = None, *, daemon: Optional[bool] = None, context: Optional[Context] = None) -> None:
        super().__init__(name, plugin, daemon=daemon, context=context)
        self.server = Server(config)

    def close(self, timeout: Optional[float] = None, block: bool = True) -> None:
        self.server.should_exit = True
        super().close(timeout, block)

    async def main(self) -> None:
        config = self.server.config
        if not config.loaded:
            config.load()
        self.server.lifespan = config.lifespan_class(config)
        await self.server.startup()
        if not self.server.should_exit:
            await self.server.main_loop()
        if self.server.started:
            await self.server.shutdown()


__all__ = [
    'ServerThread',
]