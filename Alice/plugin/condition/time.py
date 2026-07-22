from datetime import datetime

from Alice.core.plugin import Action, Condition, ConditionType, Tick, TriggerRecord


def Interval(second: int = 60, minute: int = 0, hour: int = 0) -> Condition:
    time = hour*3600 + minute*60 + second
    next_time = datetime.now().timestamp() + time
    async def condition(action: Action, tick: Tick, record: TriggerRecord) -> bool:
        nonlocal next_time
        if tick.event.time > next_time:
            next_time += time
            return True
        return False
    
    desc = '每'
    if hour:
        desc += f'{hour}时'
    if minute:
        desc += f'{minute}分'
    if second:
        desc += f'{second}秒'
    return Condition(condition, desc, ConditionType.TIME)


def SetAlarm(hour: int = 0, minute: int = 0, second: int = 0, ignore_newly_created: bool = True) -> Condition:
    now = datetime.now()
    next_time = int(datetime(now.year, now.month, now.day, hour, minute, second).timestamp())
    if not ignore_newly_created and now.timestamp() > next_time:
        next_time += 86400
    async def condition(action: Action, tick: Tick, record: TriggerRecord) -> bool:
        nonlocal next_time
        if tick.event.time > next_time:
            next_time += 86400
            return True
        return False
    
    return Condition(condition, f'每天{hour}时{minute}分{second}秒', ConditionType.TIME)


def CoolDown(second: int = 60, minute: int = 0, hour: int = 0, ) -> Condition:
    time = hour*3600 + minute*60 + second
    async def condition(action: Action, tick: Tick, record: TriggerRecord) -> bool:
        nonlocal time
        return tick.event.time - record.trigger.last > time
    
    return Condition(condition, f'在{hour}时{minute}分{second}秒后', ConditionType.TIME)


__all__ = [
    'Interval',
    'SetAlarm',
    'CoolDown',
]