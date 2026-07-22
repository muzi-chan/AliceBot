from asyncio import AbstractEventLoop, Queue, get_running_loop, sleep
from collections import deque

from time import monotonic
from typing import Any, TYPE_CHECKING, Optional

from Alice.core.event import AliceBotEvent

if TYPE_CHECKING:
    from Alice.core.bot.bot import AliceBot
    from Alice.core.core import AliceCore
    from Alice.core.event import AliceEvent
    from Alice.core.plugin.trigger import Trigger, TriggerGroup


class Tick:
    '''# 工作帧'''
    __slots__ = (
        '_started', '_starting_time', '_finished_time', '_block_triggers', '_ordinal_triggers',
        'worker', 'loop', 'bot', 'event', 'extra', 'cached_condition',
        'error_triggers', 'unused_triggers', 'success_triggers', 'processing_triggers', 'block_trigger'
    )
    _started: bool
    _starting_time: Optional[float]
    _finished_time: Optional[float]
    _block_triggers: list[Trigger]
    _ordinal_triggers: list[Trigger]
    worker: Worker
    '''## 所属工作者'''
    loop: AbstractEventLoop
    '''## 事件循环'''
    bot: Optional[AliceBot]
    '''## 事件'''
    event: AliceEvent
    '''## 事件'''
    extra: dict[Any, Any]
    '''## 额外信息'''
    cached_condition: dict[str, bool]
    '''## 缓存条件结果'''
    triggers: list[Trigger]
    '''## 当前帧所有触发器'''
    error_triggers: dict[int, Trigger]
    '''## 错误结束的触发器'''
    unused_triggers: dict[int, Trigger]
    '''## 未被触发的触发器'''
    success_triggers: dict[int, Trigger]
    '''## 成功结束的触发器'''
    processing_triggers: dict[int, Trigger]
    '''## 正在处理的触发器'''
    block_trigger: Optional[Trigger]
    '''## 触发阻塞的触发器'''
    
    def __init__(self, worker: Worker, loop: AbstractEventLoop, bot: Optional[AliceBot], event: AliceEvent, trigger_group: TriggerGroup) -> None:
        self._started = False
        self._starting_time = None
        self._finished_time = None
        self._block_triggers = trigger_group.block
        self._ordinal_triggers = trigger_group.ordinal
        self.worker = worker
        self.loop = loop
        self.bot = bot
        self.event = event
        self.extra = dict()
        self.cached_condition = dict()
        self.error_triggers = dict()
        self.unused_triggers = dict()
        self.success_triggers = dict()
        self.processing_triggers = dict()
        self.block_trigger = None
    
    async def __call__(self) -> Any:
        assert self._started == False
        self._started = True
        self._starting_time = monotonic()
        for trigger in self._block_triggers:
            await trigger(self)
        for trigger in self._ordinal_triggers:
            await trigger(self)
        self._finished_time = monotonic()
        
    @property
    def cost_time(self) -> float:
        if self._starting_time is None:
            return 0
        if self._finished_time is None:
            return monotonic() - self._starting_time
        return self._finished_time - self._starting_time


class Worker:
    
    __slots__ = ('_ident', '_core', '_loop', '_closing', '_running', '_actives', '_waiting', '_tick_costs', '_tick_times', '_tick_queue', '_atc_ema')
    
    _ident: int
    _core: AliceCore
    _loop: AbstractEventLoop
    _closing: bool
    _running: bool
    _actives: int
    _waiting: int
    _atc_ema: float
    _tick_costs: deque[float]
    _tick_times: deque[float]
    _tick_queue: Queue[Tick]

    def __init__(self, ident: int, core: AliceCore) -> None:
        self._ident = ident
        self._core = core
        self._closing = False
        self._running = False
        self._actives = 0
        self._waiting = 0
        self._atc_ema = 0
        self._tick_costs = deque(maxlen=7)
        self._tick_times = deque(maxlen=7)
        self._tick_costs.append(0)
        self._tick_times.append(monotonic())

    def __call__(self, event: AliceEvent, trigger_group: TriggerGroup) -> Any:
        self._waiting += 1
        bot = event.bot if isinstance(event, AliceBotEvent) else None
        tick = Tick(self, self._loop, bot, event, trigger_group)
        self._tick_queue.put_nowait(tick)

    async def _tick(self, tick: Tick) -> None:
        await tick()
        cost = tick.cost_time
        self._tick_costs.append(cost)
        self._tick_times.append(monotonic())
        self._actives -= 1
        self._waiting -= 1
        self._atc_ema = 0.3*cost + 0.7*self._atc_ema
        
    @property
    def ident(self) -> int:
        '''## 唯一编号'''
        return self._ident
    
    @property
    def actives(self) -> int:
        '''## 活动帧数'''
        return self._actives
    
    @property
    def waiting(self) -> int:
        '''## 等待帧数'''
        return self._waiting
    
    @property
    def queued(self) -> int:
        '''## 排队帧数'''
        return self._waiting - self._actives
    
    @property
    def load(self) -> int:
        '''## 综合负载'''
        return self._actives + self._waiting
    
    @property
    def atc(self) -> float:
        '''## 平均帧耗时'''
        return self._atc_ema
    
    @property
    def tps(self) -> float:
        '''## 每秒帧数'''
        times = tuple(self._tick_times)
        length = len(times)
        if length < 2:
            return 0.0
        elapsed = times[-1] - times[0]
        return (length-1) / elapsed
    
    def start(self) -> None:
        if self._running:
            return
        self._closing = False
        self._running = True
        self._tick_queue = Queue()
        self._core.plugin_manager._append_worker(self) # type: ignore

    def close(self) -> None:
        if not self._running:
            return
        self._closing = True
        self._running = False
    
    async def loop(self) -> None:
        loop = get_running_loop()
        self._loop = loop
        while self._running:
            if self._actives >= self._core.config.plugin.max_active_ticks:
                await sleep(0)
                continue
            if self._tick_queue.empty():
                await sleep(0.2)
                continue
            tick = self._tick_queue.get_nowait()
            loop.create_task(self._tick(tick))
            self._actives += 1
        
        while self._closing:
            if self._actives >= self._core.config.plugin.max_active_ticks:
                await sleep(0)
                continue
            if self._tick_queue.empty():
                self._tick_queue.shutdown()
                break
            tick = self._tick_queue.get_nowait()
            loop.create_task(self._tick(tick))
            self._actives += 1
        
        while self._actives > 0:
            await sleep(0.2)
        self._core.plugin_manager._remove_worker(self) # type: ignore


__all__ = [
    'Tick',
    'Worker',
]