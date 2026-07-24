from typing import Optional

from Alice.core.plugin import Action, Condition, ConditionType, Tick, TriggerRecord


async def _at_me(action: Action, tick: Tick, record: TriggerRecord) -> bool:
    return getattr(tick.event, 'at_me', False)

async def _call_me(action: Action, tick: Tick, record: TriggerRecord) -> bool:
    bot = action.bot
    if bot is None:
        return False
    pure_text: Optional[str] = getattr(tick.event, 'pure_text', None)
    if not pure_text:
        return False
    for nickname in bot.data.nicknames:
        if pure_text.startswith(nickname):
            return True
    return False

AT_ME = Condition(_at_me, '机器人被@', ConditionType.OTHER, 'at_me')
'''## 机器人被@'''

CALL_ME = Condition(_call_me, '消息以机器人昵称开头', ConditionType.OTHER, 'call_me')
'''## 消息以机器人昵称开头'''


__all__ = [
    'AT_ME',
]