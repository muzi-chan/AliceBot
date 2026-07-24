from datetime import datetime
from typing import Callable, Literal, Optional, Union

from Alice.core.plugin import Action, Condition, ConditionType, Tick, TriggerRecord


def Interval(second: int = 60, minute: int = 0, hour: int = 0) -> Condition:
    '''
    ## 创建一个间隔条件
    
    ---
    ### 参数
    * hour: 时
    * minute: 分
    * second: 秒
    '''
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
    '''
    ## 创建一个定时条件
    
    ---
    ### 参数
    * hour: 时
    * minute: 分
    * second: 秒
    * ignore_newly_created: 忽略创建时触发
    '''
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

def Frequency(second: int = 10, times: int = 1, mode: Literal['group', 'user', 'session', 'trigger'] = 'user', prompt: Optional[Union[str, Callable[[int, int, float], str]]] = None, clean_interval: int = 30) -> Condition:
    '''
    ## 创建一个频率条件
    
    ---
    ### 参数
    * second: 时长(s)
    * times: 设定时长内最大触发次数
    * mode: 计时模式
        - group: 群聊共用一个计时器
        - user: 用户的所有会话共用一个计时器
        - session: 用户的每个会话单独使用一个计时器
        - trigger: 所有会话共用一个计时器
    * prompt: 未满足频率限制时发送的内容, 如果bot不可用则跳过, 如果为函数, 三个参数分别为: 时长, 已触发次数, 下次可用时间戳
    * clean_interval: 清理记录的时间间隔
    '''
    assert second > 1
    time = second
    next_clean_time = datetime.now().timestamp() + clean_interval
    ACTIVITY: dict[str, tuple[float, int, bool]] = dict()
    def cleanup(event_time: float) -> None:
        nonlocal next_clean_time
        if event_time < next_clean_time:
            return
        next_clean_time = event_time + clean_interval
        for k, (next_time, current_times, sent) in ACTIVITY.copy().items():
            if (dt := event_time - next_time) > time:
                ACTIVITY[k] = (event_time + time, current_times - int(dt / time), sent)
            if current_times <= 0:
                del ACTIVITY[k]
                
    def check_and_record(key: str, event_time: float) -> bool:
        next_time, current_times, _ = ACTIVITY.get(key, (event_time + time, 0, False))
        if (dt := event_time - next_time) > time:
            current_times -= int(dt / time)
            next_time = event_time + time
        if current_times >= times:
            return False
        current_times = (0 if current_times < 0 else current_times) + 1
        ACTIVITY[key] = (next_time, current_times, False)
        return True
    
    async def send_prompt(key: str, action: Action) -> None:
        if prompt is None:
            return
        if action.bot is None:
            return
        record = ACTIVITY.get(key, None)
        if record is None:
            return
        next_time, current_times, sent = record
        if sent:
            return
        if isinstance(prompt, str):
            text = prompt
        else:
            text = prompt(second, times, next_time)
        ACTIVITY[key] = (next_time, current_times, True)
        await action.send(text)
    
    if mode == 'group':
        async def condition(action: Action, tick: Tick, record: TriggerRecord) -> bool:
            event_time = tick.event.time
            cleanup(event_time)
            group_id = getattr(tick.event, 'group_id', None)
            if group_id is None:
                return True
            key = str(group_id)
            check = check_and_record(key, event_time)
            if not check:
                await send_prompt(key, action)
            return check
    elif mode == 'user':
        async def condition(action: Action, tick: Tick, record: TriggerRecord) -> bool:
            event_time = tick.event.time
            cleanup(event_time)
            user_id = getattr(tick.event, 'user_id', None)
            if user_id is None:
                return True
            key = str(user_id)
            check = check_and_record(key, event_time)
            if not check:
                await send_prompt(key, action)
            return check
    elif mode == 'session':
        async def condition(action: Action, tick: Tick, record: TriggerRecord) -> bool:
            event_time = tick.event.time
            cleanup(event_time)
            group_id = getattr(tick.event, 'group_id', None)
            user_id = getattr(tick.event, 'user_id', None)
            if group_id is None or user_id is None:
                return True
            key = f'{group_id}_{user_id}'
            check = check_and_record(key, event_time)
            if not check:
                await send_prompt(key, action)
            return check
    else:
        async def condition(action: Action, tick: Tick, record: TriggerRecord) -> bool:
            event_time = tick.event.time
            cleanup(event_time)
            check = check_and_record('trigger', event_time)
            if not check:
                await send_prompt('trigger', action)
            return check
        
    return Condition(condition, f'频率{times}/{second}', ConditionType.TIME)


__all__ = [
    'Interval',
    'SetAlarm',
    'Frequency',
]