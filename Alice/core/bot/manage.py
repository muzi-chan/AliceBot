from typing import TYPE_CHECKING

from Alice.config import AliceWebSocketConfig
from Alice.core.bot.bot import AliceBot
from Alice.core.bot.thread import AliceBotWebSocketServerThread

if TYPE_CHECKING:
    from Alice.core import AliceCore


class AliceBotManager:
    '''# 机器人管理器'''
    __slots__ = ('_core', '_bots', '_app', '_servers')
    
    _core: AliceCore
    _bots: dict[int, AliceBot]
    _servers: dict[int, AliceBotWebSocketServerThread]
    
    def __init__(self, core: AliceCore) -> None:
        self._core = core
        self._bots = dict()
        self._servers = dict()
    
    def _append_bot(self, bot: AliceBot) -> None:
        self._bots.setdefault(bot.account, bot)
    
    def _remove_bot(self, bot: AliceBot) -> None:
        self._bots.pop(bot.account, bot)

    def _append_server(self, server: AliceBotWebSocketServerThread) -> None:
        self._servers.setdefault(id(server), server)
    
    def _remove_server(self, server: AliceBotWebSocketServerThread) -> None:
        self._servers.pop(id(server), None)

    @property
    def bots(self) -> dict[int, AliceBot]:
        '''## 所有bot实例'''
        return self._bots

    @property
    def servers(self) -> list[AliceBotWebSocketServerThread]:
        '''## 所有WebSocket服务线程'''
        return list(self._servers.values())
    
    def create_server(self, config: AliceWebSocketConfig, immediate: bool = True) -> AliceBotWebSocketServerThread:
        server = AliceBotWebSocketServerThread(config)
        if immediate:
            server.start()
        return server
    
    def load_bots(self) -> None:
        for path in self._core.path.bots.iterdir():
            if not path.is_dir():
                continue
            if not path.stem.isdigit():
                continue
            bot = AliceBot(int(path.stem))
            self._bots.setdefault(bot.account, bot)
            bot.data.load()
    
    def save_bots(self) -> None:
        for bot in self.bots.values():
            bot.data.save()


__all__ = [
    'AliceBotManager',
]