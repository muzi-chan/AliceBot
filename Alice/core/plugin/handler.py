from typing import Any, Awaitable, Callable, Generic, Optional, TypeVar, Union, TYPE_CHECKING

from Alice.core.plugin.condition import Condition, ConditionGroup

if TYPE_CHECKING:
    from Alice.core.plugin.action import Action
    from Alice.core.plugin.condition import Condition
    from Alice.core.plugin.trigger import Trigger, TriggerRecord
    from Alice.core.plugin.worker import Tick


TR = TypeVar('TR', bound='TriggerRecord', default='TriggerRecord')
HandlerCallable = Callable[['Action', 'Tick', TR], Awaitable[Any]]


class Handler(Generic[TR]):
    '''# 处理流程对象'''
    __slots__ = ('_priority', '_trigger', 'func', 'desc', 'condition', 'ignore_exception')
    
    _priority: int
    _trigger: Trigger
    func: HandlerCallable[TR]
    '''## 事件处理函数'''
    desc: str
    '''## 描述'''
    condition: Optional[ConditionGroup]
    '''## 条件组'''
    ignore_exception: bool
    
    def __init__(self, func: HandlerCallable[TR], desc: Optional[str], condition: Optional[Union[Condition, ConditionGroup]], trigger: Trigger, priority: int = 100, ignore_exception: bool = False) -> None:
        self._priority = priority
        self._trigger = trigger
        self.func = func
        self.desc = desc or '无'
        if isinstance(condition, ConditionGroup):
            self.condition = ConditionGroup() + condition
        elif isinstance(condition, Condition):
            self.condition = ConditionGroup([condition])
        else:
            self.condition = None
        self.ignore_exception = ignore_exception
    
    @property
    def priority(self) -> int:
        '''## 优先度'''
        return self._priority

    @priority.setter
    def priority(self, priority: int) -> None:
        self._priority = priority
        self._trigger.handlers.sort(key=lambda handler: handler.priority)
    
    @property
    def trigger(self) -> Trigger:
        '''## 所属触发器'''
        return self._trigger

    @property
    def schema(self) -> dict[str, Any]:
        '''## 纲要'''
        return {'desc': self.desc, 'condition': self.condition.schema if self.condition else None}

    async def __call__(self, action: Action, tick: Tick, record: TR) -> Any:
        if self.condition is not None and not await self.condition(action, tick, record):
            return
        await self.func(action, tick, record)


__all__ = [
    'Handler',
    'HandlerCallable',
]