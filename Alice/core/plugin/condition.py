from enum import IntEnum

from typing import Any, Iterable, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from Alice.core.plugin.action import Action
    from Alice.core.plugin.handler import HandlerCallable
    from Alice.core.plugin.trigger import TriggerRecord, TR
    from Alice.core.plugin.worker import Tick


class ConditionType(IntEnum):
    OTHER = 0
    EVENT = 1
    ROLE = 2
    TEXT = 3
    TIME = 4


class Condition:
    '''# 条件'''
    __slots__ = ('func', 'type', 'desc', 'ident', '_invert')
    
    func: HandlerCallable
    desc: str
    type: ConditionType
    ident: str
    _invert: bool
    
    def __init__(self, func: HandlerCallable[TR], desc: str, type: ConditionType = ConditionType.OTHER, ident: Optional[str] = None, invert: bool = False) -> None:
        self._invert = invert
        self.func = func # type: ignore
        self.type = type
        self.desc = desc
        self.ident = ident or str(id(self))
    
    def __and__(self, other: Union[Condition, ConditionGroup]) -> ConditionGroup:
        if isinstance(other, Condition):
            return ConditionGroup([self, other])
        return ConditionGroup([self, *other.ac], other.oc, other.ag, other.og)
    
    def __or__(self, other: Union[Condition, ConditionGroup]) -> ConditionGroup:
        if isinstance(other, Condition):
            return ConditionGroup(oc=[self, other])
        return ConditionGroup(other.ac, [self, *other.oc], other.ag, other.og)
    
    def __invert__(self) -> Condition:
        ident = self.ident.lstrip('~') if self.ident.startswith('~') else self.ident + '~'
        return Condition(self.func, self.desc, self.type, ident, not self._invert)
    
    async def __call__(self, action: Action, tick: Tick, record: TriggerRecord) -> bool:
        if (cached := tick.cached_condition.get(self.ident, None)) is not None:
            return cached
        result = await self.func(action, tick, record)
        result = not result if self._invert else result
        tick.cached_condition[self.ident] = result
        return result

    @property
    def schema(self) -> dict[str, Any]:
        '''## 纲要'''
        return {'type': self.type.value, 'desc': self.desc, 'invert': self._invert}


class ConditionGroup:
    '''# 条件组'''
    __slots__ = ('ac', 'oc', 'ag', 'og')
    
    ac: set[Condition]
    '''## 所有与条件'''
    oc: set[Condition]
    '''## 所有或条件'''
    ag: set[ConditionGroup]
    '''## 所有与条件组'''
    og: set[ConditionGroup]
    '''## 所有或条件组'''
    
    def __init__(self, ac: Optional[Iterable[Condition]] = None, oc: Optional[Iterable[Condition]] = None, ag: Optional[Iterable[ConditionGroup]] = None, og: Optional[Iterable[ConditionGroup]] = None) -> None:
        self.ac = set() if ac is None else set(ac)
        self.oc = set() if oc is None else set(oc)
        self.ag = set() if ag is None else set(ag)
        self.og = set() if og is None else set(og)
    
    def __invert__(self) -> ConditionGroup:
        ac = (~c for c in self.ac)
        oc = (~c for c in self.oc)
        ag = (~g for g in self.ag)
        og = (~g for g in self.og)
        return ConditionGroup(ac, oc, ag, og)
    
    def __add__(self, other: ConditionGroup) -> ConditionGroup:
        return ConditionGroup([*self.ac, *other.ac], [*self.oc, *other.oc], [*self.ag, *other.ag], [*self.og, *other.og])
    
    def __and__(self, other: Union[Condition, ConditionGroup]) -> ConditionGroup:
        if isinstance(other, Condition):
            return ConditionGroup([*self.ac, other], self.oc, self.ag, self.og)
        return ConditionGroup(ag=[self, other])
    
    def __or__(self, other: Union[Condition, ConditionGroup]) -> ConditionGroup:
        if isinstance(other, Condition):
            return ConditionGroup(self.ac, [*self.oc, other], self.ag, self.og)
        return ConditionGroup(og=[self, other])
    
    async def __call__(self, action: Action, tick: Tick, record: TriggerRecord) -> bool:
        for condition in self.ac:
            if not await condition(action, tick, record):
                return False
        if self.oc:
            for condition in self.oc:
                if await condition(action, tick, record):
                    break
            else:
                return False
        for group in self.ag:
            if not await group(action, tick, record):
                return False
        if self.og:
            for group in self.og:
                if await group(action, tick, record):
                    break
            else:
                return False
        return True
    
    @property
    def schema(self) -> dict[str, Any]:
        '''## 纲要'''
        return {'ac': [c.schema for c in self.ac], 'oc': [c.schema for c in self.oc], 'ag': [g.schema for g in self.ag], 'og': [g.schema for g in self.og]}


__all__ = [
    'Condition',
    'ConditionGroup',
    'ConditionType',
]