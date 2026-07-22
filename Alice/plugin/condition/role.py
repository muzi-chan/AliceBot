from Alice.core.plugin import Action, Condition, ConditionType, Tick, TriggerRecord
from Alice.onebot.event import Event
from Alice.onebot.event._event import GroupMessageEvent



async def _friend(action: Action, tick: Tick, record: TriggerRecord) -> bool:
    event = tick.event
    if not isinstance(event, Event):
        return False
    user_id = getattr(event, 'user_id', None)
    return user_id in event.bot.data.friends

async def _group_owner(action: Action, tick: Tick, record: TriggerRecord) -> bool:
    event = tick.event
    if not isinstance(event, Event):
        return False
    if isinstance(event, GroupMessageEvent):
        role = event.sender.role
        if role is not None:
            return role == 'owner'
    bot = event.bot
    user_id = getattr(event, 'user_id', None)
    group_id = getattr(event, 'group_id', None)
    if user_id is None or group_id is None:
        return False
    group = bot.data.groups.get(group_id, None)
    if group is None:
        return False
    return user_id == group.owner

async def _group_admin(action: Action, tick: Tick, record: TriggerRecord) -> bool:
    event = tick.event
    if not isinstance(event, Event):
        return False
    if isinstance(event, GroupMessageEvent):
        role = event.sender.role
        if role is not None:
            return role == 'admin'
    bot = event.bot
    user_id = getattr(event, 'user_id', None)
    group_id = getattr(event, 'group_id', None)
    if user_id is None or group_id is None:
        return False
    group = bot.data.groups.get(group_id, None)
    if group is None:
        return False
    return user_id in group.admin

async def _group_owner_or_admin(action: Action, tick: Tick, record: TriggerRecord) -> bool:
    event = tick.event
    if not isinstance(event, Event):
        return False
    if isinstance(event, GroupMessageEvent):
        role = event.sender.role
        if role is not None:
            return role == 'owner' or role == 'admin'
    bot = event.bot
    user_id = getattr(event, 'user_id', None)
    group_id = getattr(event, 'group_id', None)
    if user_id is None or group_id is None:
        return False
    group = bot.data.groups.get(group_id, None)
    if group is None:
        return False
    return user_id == group.owner or user_id in group.admin

async def _bot_is_group_owner(action: Action, tick: Tick, record: TriggerRecord) -> bool:
    event = tick.event
    if not isinstance(event, Event):
        return False
    bot = event.bot
    group_id = getattr(event, 'group_id', None)
    return group_id is not None and bot.account in bot.data.owned_groups

async def _bot_is_group_admin(action: Action, tick: Tick, record: TriggerRecord) -> bool:
    event = tick.event
    if not isinstance(event, Event):
        return False
    bot = event.bot
    group_id = getattr(event, 'group_id', None)
    return group_id is not None and bot.account in bot.data.admin_groups

async def _bot_is_group_owner_or_admin(action: Action, tick: Tick, record: TriggerRecord) -> bool:
    event = tick.event
    if not isinstance(event, Event):
        return False
    bot = event.bot
    group_id = getattr(event, 'group_id', None)
    return group_id is not None and (bot.account in bot.data.admin_groups or bot.account in bot.data.admin_groups)


ROLE_FRIEND                        = Condition(_friend, '来自好友', ConditionType.ROLE, 'is_friend')
'''## 来自好友'''
ROLE_GROUP_OWNER                   = Condition(_group_owner, '来自群主', ConditionType.ROLE, 'is_group_owner')
'''## 来自群主'''
ROLE_GROUP_ADMIN                   = Condition(_group_admin, '来自群管理员', ConditionType.ROLE, 'is_group_admin')
'''## 来自群管理员'''
ROLE_GROUP_OWNER_OR_ADMIN          = Condition(_group_owner_or_admin, '来自群主或群管理员', ConditionType.ROLE, 'is_group_owner_or_admin')
'''## 来自群主或群管理员'''
ROLE_BOT_IS_GROUP_OWNER            = Condition(_bot_is_group_owner, '机器人是群主', ConditionType.ROLE, 'bot_is_group_owner')
'''## 机器人是群主'''
ROLE_BOT_IS_GROUP_ADMIN            = Condition(_bot_is_group_admin, '机器人是群管理员', ConditionType.ROLE, 'bot_is_group_admin')
'''## 机器人是群管理员'''
ROLE_BOT_IS_GROUP_OWNER_OR_ADMIN   = Condition(_bot_is_group_owner_or_admin, '机器人是群主或群管理员', ConditionType.ROLE, 'bot_is_group_owner_or_admin')
'''## 机器人是群主或群管理员'''


__all__ = [
    'ROLE_FRIEND',
    'ROLE_GROUP_OWNER',
    'ROLE_GROUP_ADMIN',
    'ROLE_GROUP_OWNER_OR_ADMIN',
    'ROLE_BOT_IS_GROUP_OWNER',
    'ROLE_BOT_IS_GROUP_ADMIN',
    'ROLE_BOT_IS_GROUP_OWNER_OR_ADMIN',
]