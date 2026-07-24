from time import time
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from Alice.core.bot import AliceBot
    from Alice.core.plugin import Plugin


class AliceEvent(BaseModel):
    '''# Alice统一事件'''
    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)
    time: float = Field(default_factory=time)
    '''# 事件时间'''


class AliceCoreClosingEvent(AliceEvent):
    '''# Alice核心关闭事件'''


class AliceCoreIntervalEvent(AliceEvent):
    '''# 间歇事件'''


class AlicePluginEvent(AliceEvent):
    '''# 插件事件'''
    plugin: Plugin
    '''# 涉及插件'''


class AlicePluginLoadedEvent(AlicePluginEvent):
    '''# 插件加载事件'''


class AlicePluginUnLoadedEvent(AlicePluginEvent):
    '''# 插件卸载事件'''


class AliceBotEvent(AliceEvent):
    '''# 机器人事件'''
    bot: AliceBot
    '''# 事件来源机器人'''


class AliceBotConnectEvent(AliceBotEvent):
    '''# 机器人连接成功事件'''


class AliceBotDisConnectEvent(AliceBotEvent):
    '''# 机器人断开连接事件'''


__all__ = [
    'AliceEvent',
    'AliceCoreIntervalEvent',
    'AlicePluginEvent',
    'AlicePluginLoadedEvent',
    'AlicePluginUnLoadedEvent',
    'AliceBotEvent',
    'AliceBotConnectEvent',
    'AliceBotDisConnectEvent',
]