from typing import TYPE_CHECKING, Optional

from Alice.exception import ActionDone

if TYPE_CHECKING:
    from Alice.core.bot.bot import AliceBot
    from Alice.core.plugin.worker import Tick


class Action:
    
    bot: Optional[AliceBot]
    tick: Tick
    
    def __init__(self, tick: Tick) -> None:
        self.tick = tick
        self.bot = tick.bot
    
    async def send(self):
        pass
    
    async def done(self):
        raise ActionDone
    
    async def recv(self, timeout: float = 60):
        pass

    async def call_api(self):
        pass


__all__ = [
    'Action',
]