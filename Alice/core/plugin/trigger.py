from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Union, TYPE_CHECKING, overload

from Alice.core.plugin.action import Action
from Alice.core.plugin.condition import Condition, ConditionGroup
from Alice.core.plugin.handler import Handler, HandlerCallable, TR
from Alice.core.plugin.utils import current_plugin, get_core, get_plugin_from_frame
from Alice.exception import ActionDone

if TYPE_CHECKING:
    from Alice.core.plugin.plugin import Plugin
    from Alice.core.plugin.worker import Tick


@dataclass(repr=False, eq=False, slots=True)
class TriggerGroup:
    block: list[Trigger] = field(default_factory=list) # type: ignore
    ordinal: list[Trigger] = field(default_factory=list) # type: ignore


class TriggerRecord:
    
    __slots__ = ('__data__', 'trigger')
    
    __data__: dict[Any, Any]
    trigger: Trigger
    
    def __init__(self, trigger: Trigger) -> None:
        self.__data__ = dict()
        self.trigger = trigger
    
    @property
    def data(self) -> dict[Any, Any]:
        return self.__data__
    
    def __delattr__(self, name: str) -> None:
        self.__data__.pop(name, None)
    
    def __getattr__(self, name: str) -> Optional[Any]:
        return self.__data__.get(name, None)
    
    def __setattr__(self, name: str, value: Any) -> None:
        self.__data__[name] = value
    

class Trigger:
    '''
    # 触发器
    
    ---
    处理顺序: 
    * `block = True` 并根据 `priority` 排序
    * 剩余根据 `priority` 排序
    '''
    __slots__ = ('_priority', '_block', '_last', '_ident', 'name', 'desc', 'plugin', 'condition', 'handlers')
    
    _priority: int
    _block: bool
    _last: float
    _ident: int
    name: str
    '''## 名字'''
    desc: str
    '''## 说明'''
    plugin: Plugin
    '''## 所属插件'''
    condition: Optional[ConditionGroup]
    '''## 条件组'''
    handlers: list[Handler]
    

    def __init__(self, condition: Optional[Union[Condition, ConditionGroup]] = None, name: Optional[str] = None, desc: Optional[str] = None, plugin: Optional[Plugin] = None, priority: int = 100, block: bool = False) -> None:
        '''
        ## 触发器初始化
        
        ---
        ### 参数
        * condition: 条件
        * name: 名字 默认为 id
        * desc: 描述
        * plugin: 所属插件
        * priority: 优先度, 越小优先度越高
        * block: 是否为并发触发器, 为 `True` 且通过条件检查后会阻止后续触发器
        * record_factory: 触发器记录工厂, 用于生成自定义触发器记录
        '''
        self._ident = id(self)
        self.name = name or str(self.ident)
        self.desc = desc or ''
        plugin = current_plugin() or get_plugin_from_frame() if plugin is None else plugin
        assert plugin is not None, '请显式的设置plugin'
        self.plugin = plugin
        if isinstance(condition, ConditionGroup):
            self.condition = ConditionGroup() + condition
        elif isinstance(condition, Condition):
            self.condition = ConditionGroup([condition])
        else:
            self.condition = ConditionGroup()
        self._priority = priority
        self._block = block
        self._last = -1
        self.handlers = list()
        self._register()
    
    async def __call__(self, tick: Tick) -> Any:
        tid = self._ident
        if tick.block_trigger is not None:
            tick.unused_triggers.setdefault(tid, self)
            return
        action = Action(tick)
        record = TriggerRecord(trigger=self)
        try:
            if self.condition is not None and not await self.condition(action, tick, record):
                tick.unused_triggers.setdefault(tid, self)
                return
        except:
            tick.error_triggers.setdefault(tid, self)
            return
        self._last = tick.event.time
        tick.processing_triggers.setdefault(tid, self)
        try:
            for handler in self.handlers.copy():
                try:
                    await handler(action, tick, record)
                except ActionDone:
                    break
                except Exception as e:
                    if not handler.ignore_exception:
                        raise Exception from e
        except:
            tick.error_triggers.setdefault(tid, self)
        else:
            tick.processing_triggers.pop(tid)
            tick.success_triggers.setdefault(tid, self)
        if self.block:
            tick.block_trigger = self

    def _update(self) -> None:
        if self.plugin.status.loaded:
            get_core().plugin_manager._build_cached_trigger_group() # type: ignore

    def _register(self) -> None:
        self.plugin.triggers.setdefault(self._ident, self)
        self._update()

    def _unregister(self) -> None:
        self.plugin.triggers.pop(self._ident, None)
        self._update()
   
    @property
    def ident(self) -> int:
        '''## 唯一编号'''
        return self._ident
    
    @property
    def priority(self) -> int:
        '''
        ## 优先度
        
        ---
        越小优先度越高
        '''
        return self._priority
    
    @priority.setter
    def priority(self, value: int) -> None:
        self._priority = value
        self._update()
    
    @property
    def block(self) -> bool:
        '''
        ## 是否为阻塞触发器
        
        ---
        为 `True` 且通过条件检查后会阻止后续触发器
        '''
        return self._block
    
    @property
    def last(self) -> float:
        '''## 上次触发时间戳'''
        return self._last
    
    @block.setter
    def block(self, value: bool) -> None:
        self._block = value
        self._update()
    
    @property
    def schema(self) -> dict[str, Any]:
        '''## 纲要'''
        return {'name': self.name, 'desc': self.desc, 'condition': self.condition.schema if self.condition else None, 'handlers': [handler.schema for handler in self.handlers.copy()]}
    
    def remove(self, immediate: bool = False) -> None:
        '''
        ## 移除自身
        
        ---
        ### 参数
        * immediate: 为 `True` 时立即抛出 `RemoveTrigger` 异常, 如果当前Trigger正在处理则会直接结束处理流程
        '''
        self._unregister()
        if immediate:
            raise
    
    @overload
    def handle(self, func: HandlerCallable[TR]) -> Handler:
        '''## 添加事件处理流程装饰器'''
    
    @overload
    def handle(self, *, desc: Optional[str] = None, condition: Optional[Union[Condition, ConditionGroup]] = None, priority: int = 100, ignore_exception: bool = False) ->  Callable[..., Handler]:
        '''
        ## 添加事件处理流程装饰器
        
        ---
        ### 参数
        * desc: 说明
        * condition: 条件
        * priority: 优先度
        * ignore_exception: 忽略异常
        '''
    
    @overload
    def handle(self, *, func: HandlerCallable[TR], desc: Optional[str] = None, condition: Optional[Union[Condition, ConditionGroup]] = None, priority: int = 100, ignore_exception: bool = False) ->  Handler:
        '''
        ## 添加事件处理流程
        
        ---
        ### 参数
        * func: 事件处理函数
        * desc: 说明
        * condition: 条件
        * priority: 优先度
        * ignore_exception: 忽略异常
        '''
    
    def handle(self, func: Optional[HandlerCallable[TR]] = None, desc: Optional[str] = None, condition: Optional[Union[Condition, ConditionGroup]] = None, priority: int = 100, ignore_exception: bool = False) -> Union[Callable[..., Handler], Handler]:
        def wrap(func: HandlerCallable) -> Handler:
            handler = Handler(func, desc, condition, self, priority, ignore_exception)
            self.handlers.append(handler)
            self.handlers.sort(key=lambda handler: handler.priority)
            return handler
        
        return wrap if func is None else wrap(func) # type: ignore


__all__ = [
    'Trigger',
    'TriggerGroup',
    'TriggerRecord',
]