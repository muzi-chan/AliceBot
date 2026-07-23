from Alice.core.plugin import Action, Condition, ConditionType, Tick, TriggerRecord


async def _at_me(action: Action, tick: Tick, record: TriggerRecord) -> bool:
    return getattr(tick.event, 'at_me', False)

AT_ME = Condition(_at_me, '机器人被@', ConditionType.OTHER, 'at_me')
'''## 机器人被@'''


__all__ = [
    'AT_ME',
]