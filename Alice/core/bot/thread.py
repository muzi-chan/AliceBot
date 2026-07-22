from asyncio import Queue, get_running_loop, sleep
from contextlib import asynccontextmanager
from contextvars import Context
from json import dumps as json_dumps
from typing import Any, Optional, TYPE_CHECKING

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from uvicorn import Config

from Alice.config import AliceWebSocketConfig
from Alice.core.bot.bot import AliceBot
from Alice.core.event import AliceBotConnectEvent, AliceBotDisConnectEvent
from Alice.core.thread.server import ServerThread
from Alice.exception import APIBotNotConnected
from Alice.log import logger
from Alice.onebot.message import MessageJSONEncoder
from Alice.onebot.utils import parse_raw_onebot_event

if TYPE_CHECKING:
    from Alice.core.bot.api import AliceBotAPICall


class AliceBotWebSocketServerThread(ServerThread):
    
    _bots: dict[int, AliceBot]
    _websockets: dict[int, WebSocket]
    _calls: dict[int, AliceBotAPICall[..., Any]]
    _call_queue: Queue[AliceBotAPICall[..., Any]]
    
    def __init__(self, config: AliceWebSocketConfig, *, context: Optional[Context] = None) -> None:
        assert config.enable
        app = FastAPI()
        app.websocket(config.path, config.name)(self._websocket)
        app.router.lifespan_context = self._lifespan
        server_config = Config(app, config.host, config.port, log_config = {'version': 1, 'disable_existing_loggers': True})
        super().__init__(server_config, f'WS|{config.name}', None, daemon=False, context=context)
        self.config = config
        self._bots = dict()
        self._websockets = dict()
        self._calls = dict()
    
    @asynccontextmanager
    async def _lifespan(self, _: FastAPI):
        bot_manager = self._core.bot_manager
        bot_manager._append_server(self) # type: ignore
        logger.success(f'WebSocket Server已在[ws://{self.config.host}:{self.config.port}{self.config.path}]开启')
        yield
        bot_manager._remove_server(self) # type: ignore
    
    async def _websocket(self, websocket: WebSocket) -> None:
        await websocket.accept()
        host, port = websocket.scope.get('client', ('未知', '未知'))
        data = await websocket.receive_json()
        bot = AliceBot(-1)
        event = parse_raw_onebot_event(bot, data)
        if event is None:
            await websocket.close()
            logger.warning(f'未知客户端[{host}:{port}]尝试连接.\n{data}')
            return
        account = event.self_id
        if account in self._bots:
            bot = self._bots[account]
        elif account in self._core.bot_manager.bots:
            bot = self._core.bot_manager.bots[account]
        else:
            bot = AliceBot(account)
            self._core.bot_manager._append_bot(bot) # type: ignore
        self._bots[account] = bot
        event.bot = bot
        setattr(bot, '_server', self)
        logger.success(f'[{host}:{port}][{account}]连接成功.')
        plugin_manager = self._core.plugin_manager
        self._websockets.setdefault(bot.account, websocket)
        plugin_manager.dispatch_event(AliceBotConnectEvent(bot=bot))
        plugin_manager.dispatch_event(event)
        try:
            while True:
                data: dict[str, Any] = await websocket.receive_json()
                if (echo := data.get('echo', None)) and (call := self._calls.pop(echo, None)):
                    call.fut.set_result(data)
                elif event := parse_raw_onebot_event(bot, data):
                    plugin_manager.dispatch_event(event)
        except WebSocketDisconnect:
            logger.warning(f'[{host}:{port}][{account}]断开连接.')
        except:
            logger.error(f'[{host}:{port}][{account}]因发生错误断开连接.')
        self._bots.pop(account, None)
        self._websockets.pop(account, None)
        setattr(bot, '_server', None)
        plugin_manager.dispatch_event(AliceBotDisConnectEvent(bot=bot))

    async def _call_loop(self) -> None:
        while self._loop_running:
            if self._call_queue.empty():
                await sleep(0.2)
                continue
            call = self._call_queue.get_nowait()
            await self._send_call(call)
    
    async def _send_call(self, call: AliceBotAPICall[..., Any]) -> None:
        websocket = self._websockets.get(call.bot.account, None)
        if websocket is None:
            call.fut.set_exception(APIBotNotConnected())
            return
        self._calls[call.echo] = call
        json_data = json_dumps({'action': call.api.name, 'params': call.params, 'echo': call.echo}, cls=MessageJSONEncoder)
        await websocket.send({'type': 'websocket.send', 'text': json_data})
    
    async def main(self) -> None:
        self._call_queue = Queue()
        get_running_loop().create_task(self._call_loop())
        await super().main()

    def put_call(self, call: AliceBotAPICall[..., Any]) -> None:
        self._call_queue.put_nowait(call)
    
    @property
    def bots(self) -> dict[int, AliceBot]:
        return self._bots.copy()


__all__ = [
    'AliceBotWebSocketServerThread',
]