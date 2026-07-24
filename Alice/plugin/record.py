from re import Match

from Alice.core.plugin import TriggerRecord
from Alice.lib.commandparse import ParseResult


class CommandRecord(TriggerRecord):
    '''## 命令触发器触发时捕获数据'''
    result: ParseResult


class RegexRecord(TriggerRecord):
    '''## 正则触发器触发时捕获数据'''
    matched: Match[str]


__all__ = [
    'CommandRecord',
    'RegexRecord',
]