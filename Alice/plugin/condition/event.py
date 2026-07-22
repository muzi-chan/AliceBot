from Alice.core.event import *
from Alice.core.event import AliceCoreClosingEvent
from Alice.core.plugin import Action, Condition, ConditionType, Tick, TriggerRecord
from Alice.onebot.event import *


def _ec(event: type[AliceEvent], desc: str) -> Condition:
    async def condition(action: Action, tick: Tick, record: TriggerRecord) -> bool:
        return isinstance(tick.event, event)
    return Condition(condition, desc, ConditionType.EVENT, f'is_{event.__name__}')

#region Alice
EVENT_ALICE_CORE_CLOSING           = _ec(AliceCoreClosingEvent, 'Alice核心关闭事件')
'''## Alice核心关闭事件'''
EVENT_ALICE_CORE_INTERVAL          = _ec(AliceCoreIntervalEvent, '间歇事件')
'''## 间歇事件'''
EVENT_ALICE_PLUGIN                 = _ec(AlicePluginEvent, '插件事件')
'''## 插件事件'''
EVENT_ALICE_PLUGIN_LOADED          = _ec(AlicePluginLoadedEvent, '插件加载事件')
'''## 插件加载事件'''
EVENT_ALICE_PLUGIN_UNLOADED        = _ec(AlicePluginUnLoadedEvent, '插件卸载事件')
'''## 插件卸载事件'''
EVENT_ALICE_BOT                    = _ec(AliceBotEvent, '机器人事件')
'''## 机器人事件'''
EVENT_ALICE_BOT_CONNECT            = _ec(AliceBotConnectEvent, '机器人连接成功事件')
'''## 连接成功事件'''
EVENT_ALICE_BOT_DISCONNECT         = _ec(AliceBotDisConnectEvent, '机器人断开连接事件')
'''## 断开连接事件'''
#endregion
#region OneBot
EVENT_MESSAGE                      = _ec(MessageEvent, '消息事件')
'''## 消息事件'''
EVENT_MESSAGE_GROUP                = _ec(GroupMessageEvent, '群消息事件')
'''## 群消息事件'''
EVENT_MESSAGE_PRIVATE              = _ec(PrivateMessageEvent, '私聊消息事件')
'''## 私聊消息事件'''
EVENT_MESSAGE_SENT                 = _ec(MessageSentEvent, '消息发送事件')
'''## 消息发送事件'''
EVENT_MESSAGE_SENT_GROUP           = _ec(GroupMessageSentEvent, '群消息发送事件')
'''## 群消息发送事件'''
EVENT_MESSAGE_SENT_PRIVATE         = _ec(PrivateMessageSentEvent, '私聊消息发送事件')
'''## 私聊消息发送事件'''
EVENT_NOTICE                       = _ec(NoticeEvent, '通知事件')
'''## 通知事件'''
EVENT_NOTICE_GROUP_UPLOAD          = _ec(GroupUploadEvent, '群文件上传事件')
'''## 群文件上传事件'''
EVENT_NOTICE_GROUP_ADMIN           = _ec(GroupAdminEvent, '群管理员变动事件')
'''## 群管理员变动事件'''
EVENT_NOTICE_GROUP_DECREASE        = _ec(GroupDecreaseEvent, '群成员减少事件')
'''## 群成员减少事件'''
EVENT_NOTICE_GROUP_INCREASE        = _ec(GroupIncreaseEvent, '群成员增加事件')
'''## 群成员增加事件'''
EVENT_NOTICE_GROUP_BAN             = _ec(GroupBanEvent, '群禁言事件')
'''## 群禁言事件'''
EVENT_NOTICE_FRIEND_ADD            = _ec(FriendAddEvent, '好友添加事件')
'''## 好友添加事件'''
EVENT_NOTICE_GROUP_RECALL          = _ec(GroupRecallEvent, '群消息撤回事件')
'''## 群消息撤回事件'''
EVENT_NOTICE_FRIEND_RECALL         = _ec(FriendRecallEvent, '好友消息撤回事件')
'''## 好友消息撤回事件'''
EVENT_NOTICE_GROUP_CARD            = _ec(GroupCardEvent, '群名片变更事件')
'''## 群名片变更事件'''
EVENT_NOTICE_GROUP_ESSENCE         = _ec(GroupEssenceEvent, '群精华消息事件')
'''## 群精华消息事件'''
EVENT_NOTICE_GROUP_MSG_EMOJI_LIKE  = _ec(GroupMsgEmojiLikeEvent, '表情回应事件')
'''## 表情回应事件'''
EVENT_NOTICE_BOT_OFFLINE           = _ec(BotOfflineEvent, '机器人离线事件')
'''## 机器人离线事件'''
EVENT_NOTIFY                       = _ec(NotifyEvent, '提示事件')
'''## 提示事件'''
EVENT_NOTIFY_GROUP_NAME            = _ec(GroupNameEvent, '群名变更事件')
'''## 群名变更事件'''
EVENT_NOTIFY_GROUP_TITLE           = _ec(GroupTitleEvent, '群头衔变更事件')
'''## 群头衔变更事件'''
EVENT_NOTIFY_GROUP_GRAY_TIP        = _ec(GroupGrayTipEvent, '群灰条消息事件')
'''## 群灰条消息事件'''
EVENT_NOTIFY_POKE                  = _ec(PokeEvent, '群戳一戳事件')
'''## 群戳一戳事件'''
EVENT_NOTIFY_PROFILE_LIKE          = _ec(ProfileLikeEvent, '个人资料点赞事件')
'''## 个人资料点赞事件'''
EVENT_NOTIFY_INPUT_STATUS          = _ec(InputStatusEvent, '输入状态事件')
'''## 输入状态事件'''
EVENT_REQUEST                      = _ec(RequestEvent, '请求事件')
'''## 请求事件'''
EVENT_REQUEST_FRIEND               = _ec(FriendRequestEvent, '加好友请求事件')
'''## 加好友请求事件'''
EVENT_REQUEST_GROUP                = _ec(GroupRequestEvent, '加群请求/邀请事件')
'''## 加群请求/邀请事件'''
EVENT_META                         = _ec(MetaEvent, '元事件')
'''## 元事件'''
EVENT_META_HEARTBEAT               = _ec(HeartbeatMetaEvent, '心跳事件')
'''## 心跳事件'''
EVENT_META_LIFECYCLE               = _ec(LifecycleMetaEvent, '生命周期事件')
'''## 生命周期事件'''
#endregion

__all__ = [
    'EVENT_ALICE_CORE_CLOSING',
    'EVENT_ALICE_CORE_INTERVAL',
    'EVENT_ALICE_PLUGIN',
    'EVENT_ALICE_PLUGIN_LOADED',
    'EVENT_ALICE_PLUGIN_UNLOADED',
    'EVENT_ALICE_BOT',
    'EVENT_ALICE_BOT_CONNECT',
    'EVENT_ALICE_BOT_DISCONNECT',
    'EVENT_MESSAGE',
    'EVENT_MESSAGE_GROUP',
    'EVENT_MESSAGE_PRIVATE',
    'EVENT_MESSAGE_SENT',
    'EVENT_MESSAGE_SENT_GROUP',
    'EVENT_MESSAGE_SENT_PRIVATE',
    'EVENT_NOTICE',
    'EVENT_NOTICE_GROUP_UPLOAD',
    'EVENT_NOTICE_GROUP_ADMIN',
    'EVENT_NOTICE_GROUP_DECREASE',
    'EVENT_NOTICE_GROUP_INCREASE',
    'EVENT_NOTICE_GROUP_BAN',
    'EVENT_NOTICE_FRIEND_ADD',
    'EVENT_NOTICE_GROUP_RECALL',
    'EVENT_NOTICE_FRIEND_RECALL',
    'EVENT_NOTICE_GROUP_CARD',
    'EVENT_NOTICE_GROUP_ESSENCE',
    'EVENT_NOTICE_GROUP_MSG_EMOJI_LIKE',
    'EVENT_NOTICE_BOT_OFFLINE',
    'EVENT_NOTIFY',
    'EVENT_NOTIFY_GROUP_NAME',
    'EVENT_NOTIFY_GROUP_TITLE',
    'EVENT_NOTIFY_GROUP_GRAY_TIP',
    'EVENT_NOTIFY_POKE',
    'EVENT_NOTIFY_PROFILE_LIKE',
    'EVENT_NOTIFY_INPUT_STATUS',
    'EVENT_REQUEST',
    'EVENT_REQUEST_FRIEND',
    'EVENT_REQUEST_GROUP',
    'EVENT_META',
    'EVENT_META_HEARTBEAT',
    'EVENT_META_LIFECYCLE',
]