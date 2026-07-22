from functools import cached_property
from typing import Any, Optional

from pydantic import field_validator

from Alice.core.event import AliceBotEvent
from Alice.onebot.message import Message
from Alice.onebot.event._model import File, MsgEmojiLike, Status, Sender


POST_TYPES = {'message': 'message_type', 'message_sent': 'message_type', 'meta_event': 'meta_event_type', 'notice': 'notice_type', 'request': 'request_type'}

class Event(AliceBotEvent):
    '''# 基础事件'''
    self_id: int
    '''## 收到事件的机器人 QQ 号'''
    post_type: str
    '''## 上报类型'''


#region 消息事件
class MessageEvent(Event):
    '''# 消息事件'''
    post_type: str = 'message'
    '''## 上报类型'''
    message_type: str
    '''
    ## 消息类型
    
    ---
    ### 可能的值
    * group: 群消息
    * private: 私聊消息
    '''
    sub_type: str
    '''## 消息子类型'''
    message_id: int
    '''## 消息 ID'''
    message: Message
    '''## 消息内容'''
    raw_message: str
    '''## 原始消息内容'''
    font: int
    '''## 字体'''
    sender: Sender
    '''## 发送者'''
    user_id: int
    '''## 发送者 QQ 号'''
    # 拓展
    @cached_property
    def at_me(self) -> bool:
        '''## 机器人是否被艾特'''
        return False
    
    @cached_property
    def reply_id(self) -> Optional[int]:
        '''## 被回复消息 ID'''
        if self.message.array and (segment := self.message.segments[0]).type == 'reply':
            return segment.data.get('id')
    
    @cached_property
    def pure_text(self) -> str:
        '''## 纯文本消息'''
        return ''.join([segment.data['text'] for segment in self.message.segments if segment.type == 'text'])
    
    @field_validator('message', mode='before')
    def _(cls, data: Any) -> Message:
        return Message(data)


class GroupMessageEvent(MessageEvent):
    '''# 群消息事件'''
    message_type: str = 'group'
    '''## 消息类型'''
    sub_type: str
    '''
    ## 消息子类型
    
    ---
    可能的值:
    * `normal` 正常消息
    * `anonymous` 匿名消息
    * `notice` 系统提示
    '''
    group_id: int
    '''## 群号'''
    # 拓展
    @cached_property
    def at_ids(self) -> list[int]:
        '''## 所有艾特对象'''
        return [int(segment.data['qq']) for segment in self.message.segments if segment.type == 'at']

    @cached_property
    def at_me(self) -> bool:
        return self.self_id in self.at_ids


class PrivateMessageEvent(MessageEvent):
    '''# 私聊消息事件'''
    message_type: str = 'private'
    '''## 消息类型'''
    sub_type: str
    '''
    ## 消息子类型
    
    ---
    可能的值:
    * `friend` 好友
    * `group` 群临时会话
    * `other` 其它
    '''
#endregion
#region 消息发送事件
class MessageSentEvent(Event):
    '''# 消息发送事件'''
    post_type: str = 'message_sent'
    '''## 上报类型'''


class GroupMessageSentEvent(MessageSentEvent, MessageEvent):
    '''# 群消息发送事件'''


class PrivateMessageSentEvent(MessageSentEvent, MessageEvent):
    '''# 私聊消息发送事件'''
#endregion
#region 通知事件
class NoticeEvent(Event):
    '''# 通知事件'''
    post_type: str = 'notice'
    '''## 上报类型'''
    notice_type: str
    '''## 通知类型'''


class GroupUploadEvent(NoticeEvent):
    '''# 群文件上传事件'''
    notice_type: str = 'group_upload'
    '''## 通知类型'''
    user_id: int
    '''## 发送者 QQ 号'''
    group_id: int
    '''## 群号'''
    file: File
    '''## 文件信息'''


class GroupAdminEvent(NoticeEvent):
    '''# 群管理员变动事件'''
    notice_type: str = 'group_admin'
    '''## 通知类型'''
    sub_type: str
    '''
    ## 事件子类型
    
    ---
    * `set` 设置管理员
    * `unset` 取消管理员
    '''
    user_id: int
    '''## 管理员 QQ 号'''
    group_id: int
    '''## 群号'''


class GroupDecreaseEvent(NoticeEvent):
    '''# 群成员减少事件'''
    notice_type: str = 'group_decrease'
    '''## 通知类型'''
    sub_type: str
    '''
    ## 事件子类型
    
    ---
    * `leave` 主动退群
    * `kick` 成员被踢
    * `kick_me` 登录号被踢
    * `disband` 群解散
    '''
    user_id: int
    '''## 离开者 QQ 号'''
    group_id: int
    '''## 群号'''
    operator_id: int
    '''
    ## 操作者 QQ 号
    
    ---
    如果是主动退群则和`user_id`相同
    '''


class GroupIncreaseEvent(NoticeEvent):
    '''# 群成员增加事件'''
    notice_type: str = 'group_increase'
    '''## 通知类型'''
    sub_type: str
    '''
    ## 事件子类型
    
    ---
    * `approve` 同意入群
    * `invite` 邀请入群
    '''
    user_id: int
    '''## 加入者 QQ 号'''
    group_id: int
    '''## 群号'''
    operator_id: int
    '''
    ## 操作者 QQ 号
    
    ---
    如果是主动退群则和`user_id`相同
    '''


class GroupBanEvent(NoticeEvent):
    '''# 群禁言事件'''
    notice_type: str = 'group_ban'
    '''## 通知类型'''
    sub_type: str
    '''
    ## 事件子类型
    
    ---
    * `ban` 禁言
    * `lift_ban` 解除禁言
    '''
    user_id: int
    '''## 被禁言 QQ 号'''
    group_id: int
    '''## 群号'''
    operator_id: int
    '''## 操作者 QQ 号'''
    duration: int
    '''
    ## 禁言时长
    
    ---
    单位秒
    '''


class FriendAddEvent(NoticeEvent):
    '''# 好友添加事件'''
    notice_type: str = 'friend_add'
    '''## 通知类型'''
    user_id: int
    '''## 新添加好友 QQ 号'''


class GroupRecallEvent(NoticeEvent):
    '''# 群消息撤回事件'''
    notice_type: str = 'group_recall'
    '''## 通知类型'''
    user_id: int
    '''## 消息发送者 QQ 号'''
    group_id: int
    '''## 群号'''
    operator_id: int
    '''## 操作者 QQ 号'''
    message_id: int
    '''## 被撤回的消息 ID'''


class FriendRecallEvent(NoticeEvent):
    '''# 好友消息撤回事件'''
    notice_type: str = 'friend_recall'
    '''## 通知类型'''
    user_id: int
    '''## 好友 QQ 号'''
    message_id: int
    '''## 被撤回的消息 ID'''


class GroupCardEvent(NoticeEvent):
    '''# 群名片变更通知'''
    notice_type: str = 'group_card'
    '''## 通知类型'''
    user_id: int
    '''## 修改者 QQ 号'''
    group_id: int
    '''## 群号'''
    card_new: str
    '''## 新名片'''
    card_old: str
    '''## 旧名片'''


class GroupEssenceEvent(NoticeEvent):
    '''# 群精华消息通知'''
    notice_type: str = 'essence'
    '''## 通知类型'''
    sub_type: str
    '''
    ## 事件子类型
    
    ---
    * `add` 添加
    * `delete` 删除
    '''
    user_id: int
    '''## 设置群精华用户 QQ 号'''
    group_id: int
    '''## 群号'''
    message_id: int
    '''## 群精华消息 ID'''
    sender_id: int
    '''## 群精华消息 ID'''
    operator_id: int
    '''## 操作者 QQ 号'''


class GroupMsgEmojiLikeEvent(NoticeEvent):
    '''# 表情回应通知'''
    notice_type: str = 'group_msg_emoji_like'
    '''## 通知类型'''
    user_id: int
    '''## 发送者 QQ 号'''
    group_id: int
    '''## 群号'''
    message_id: int
    '''## 消息 ID'''
    likes: list[MsgEmojiLike]
    '''## 表情回应列表'''


class BotOfflineEvent(NoticeEvent):
    '''# 机器人离线通知'''
    notice_type: str = 'bot_offline'
    '''## 通知类型'''
    user_id: int
    '''## 机器人 QQ 号'''
    tag: str
    '''## 标签'''
    message: str
    '''## 离线消息'''
#endregion
#region 提示事件
class NotifyEvent(NoticeEvent):
    '''# 提示事件'''
    notice_type: str = 'notify'
    '''## 通知类型'''
    sub_type: str
    '''## 提示类型'''


class GroupNameEvent(NotifyEvent):
    '''# 群名变更通知'''
    sub_type: str = 'group_name'
    '''## 提示类型'''
    user_id: int
    '''## 修改者 QQ 号'''
    group_id: int
    '''## 群号'''
    name_new: str
    '''## 新群名'''


class GroupTitleEvent(NotifyEvent):
    '''# 群头衔变更通知'''
    sub_type: str = 'title'
    '''## 提示类型'''
    user_id: int
    '''## 修改者 QQ 号'''
    group_id: int
    '''## 群号'''
    title: str
    '''## 新头衔'''


class GroupGrayTipEvent(NotifyEvent):
    '''# 群灰条消息通知'''
    sub_type: str = 'gray_tip'
    '''## 提示类型'''
    user_id: int
    '''## 发送者 QQ 号'''
    group_id: int
    '''## 群号'''
    message_id: int
    '''## 消息 ID'''
    busi_id: str
    '''## 业务 ID'''
    content: str
    '''## 灰条内容(JSON)'''
    raw_info: str
    '''## 原始信息'''


class PokeEvent(NotifyEvent):
    '''# 群戳一戳事件'''
    sub_type: str = 'poke'
    '''## 提示类型'''
    user_id: int
    '''## 发送者 QQ 号'''
    group_id: Optional[int] = None
    '''## 群号'''
    target_id: int
    '''## 被戳者 QQ 号'''


class ProfileLikeEvent(NotifyEvent):
    '''# 个人资料点赞通知'''
    sub_type: str = 'profile_like'
    '''## 提示类型'''
    operator_id: int
    '''## 操作者 QQ 号'''
    operator_nick: str
    '''## 操作者昵称'''
    times: int
    '''## 点赞次数'''


class InputStatusEvent(NotifyEvent):
    '''# 输入状态通知'''
    sub_type: str = 'input_status'
    '''## 提示类型'''
    status_text: str
    '''## 状态文本'''
    event_type: int
    '''## 事件类型'''
    user_id: int
    '''## 用户 QQ 号'''
    group_id: Optional[int] = None
    '''## 群号'''
#endregion
#region 请求事件
class RequestEvent(Event):
    '''# 请求事件'''
    post_type: str = 'request'
    '''## 上报类型'''
    request_type: str
    '''## 请求类型'''


class FriendRequestEvent(RequestEvent):
    '''# 加好友请求事件'''
    request_type: str = 'friend'
    '''## 请求类型'''
    user_id: int
    '''## 发送请求的 QQ 号'''
    comment: str = ''
    '''## 验证信息'''
    flag: str
    '''
    ## 请求 flag
    
    ---
    在调用处理请求的 API 时需要传入
    '''


class GroupRequestEvent(RequestEvent):
    '''# 加群请求/邀请事件'''
    request_type: str = 'group'
    '''## 请求类型'''
    sub_type: str
    '''
    ## 请求子类型
    
    ---
    * `add` 加群请求
    * `invite` 邀请登录号入群
    '''
    user_id: int
    '''## 发送请求的 QQ 号'''
    group_id: int
    '''## 群号'''
    comment: str = ''
    '''## 验证信息'''
    flag: str
    '''
    ## 请求 flag
    
    ---
    在调用处理请求的 API 时需要传入
    '''
#endregion
#region 元事件
class MetaEvent(Event):
    '''# 元事件'''
    post_type: str = 'meta_event'
    meta_event_type: str


class HeartbeatMetaEvent(MetaEvent):
    '''# 心跳事件'''
    meta_event_type: str = 'heartbeat'
    interval: int
    '''
    ## 到下次心跳的间隔
    
    ---
    单位毫秒
    '''
    status: Status
    '''## 状态信息'''


class LifecycleMetaEvent(MetaEvent):
    '''# 生命周期事件'''
    meta_event_type: str = 'lifecycle'
    '''## 元事件类型'''
    sub_type: str
    '''
    ## 事件子类型
    
    ---
    可能的值:
    * `enable` OneBot 启用
    * `disable` OneBot 停用
    * `connect` WebSocket 连接成功
    '''
#endregion

__all__ = [
    'Event',
    'MessageEvent',
    'GroupMessageEvent',
    'PrivateMessageEvent',
    'MessageSentEvent',
    'GroupMessageSentEvent',
    'PrivateMessageSentEvent',
    'NoticeEvent',
    'GroupUploadEvent',
    'GroupAdminEvent',
    'GroupDecreaseEvent',
    'GroupIncreaseEvent',
    'GroupBanEvent',
    'FriendAddEvent',
    'GroupRecallEvent',
    'FriendRecallEvent',
    'GroupCardEvent',
    'GroupEssenceEvent',
    'GroupMsgEmojiLikeEvent',
    'BotOfflineEvent',
    'NotifyEvent',
    'GroupNameEvent',
    'GroupTitleEvent',
    'GroupGrayTipEvent',
    'PokeEvent',
    'ProfileLikeEvent',
    'InputStatusEvent',
    'RequestEvent',
    'FriendRequestEvent',
    'GroupRequestEvent',
    'MetaEvent',
    'HeartbeatMetaEvent',
    'LifecycleMetaEvent',
]