from re import RegexFlag, compile
from typing import Optional

from Alice.core.plugin import Action, Condition, ConditionType, Tick
from Alice.lib.commandparse import CommandParser
from Alice.onebot.event import MessageEvent
from Alice.plugin.record import CommandRecord, RegexRecord


def Command(command: CommandParser, desc: Optional[str] = None) -> Condition:
    async def condition(action: Action, tick: Tick, record: CommandRecord) -> bool:
        event = tick.event
        if not isinstance(event, MessageEvent):
            return False
        text = event.pure_text.strip()
        result = command.parse(text)
        if result is None:
            return False
        record.result = result
        return True
    return Condition(condition, desc or f'command_{command.start}', ConditionType.TEXT)

def Regex(pattern: str, flags: RegexFlag = RegexFlag.S, desc: Optional[str] = None) -> Condition:
    compiled = compile(pattern, flags)
    async def condition(action: Action, tick: Tick, record: RegexRecord) -> bool:
        event = tick.event
        if not isinstance(event, MessageEvent):
            return False
        text = event.pure_text.strip()
        matched = compiled.search(text)
        if matched is None:
            return False
        record.matched = matched
        return True
    return Condition(condition, desc or f'regex_{pattern}', ConditionType.TEXT)


