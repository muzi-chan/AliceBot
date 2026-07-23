from functools import cached_property
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from Alice.core.bot.api import AliceBotAPIModel
from Alice.onebot.message import Message
from Alice.onebot.event._event import GroupMessageEvent, GroupMessageSentEvent, MessageEvent, PrivateMessageEvent, PrivateMessageSentEvent
from Alice.onebot.event._model import Sender


class _ChildModel(BaseModel):
    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)
    

class ModelShow(AliceBotAPIModel):
    '''# 机型展示'''
    model_show: str
    need_pay: bool


class CanSend(AliceBotAPIModel):
    '''# 是否支持发送'''
    yes: bool
    '''## 是否支持发送'''


class CheckUrlSafely(AliceBotAPIModel):
    '''# 链接安全性'''
    level: int
    '''## 安全等级'''


class CleanStreamTempFile(AliceBotAPIModel):
    '''# 清理流式传输临时文件'''
    message: str
    removed: int


class CreateFlashTask(AliceBotAPIModel):
    '''# 闪传任务'''
    fileset_id: str
    '''## 文件集 ID'''
    task_id: str
    '''## 任务 ID'''


class DownloadFile(AliceBotAPIModel):
    '''# 下载文件'''
    file: Path


class DownloadFileset(AliceBotAPIModel):
    '''# 闪传文件下载直链'''
    url: str
    '''## 下载直链'''
    file_name: str
    '''## 文件名'''
    file_size: str
    '''## 文件大小'''


class _EmojiLikesList(_ChildModel):
    tiny_id: int = Field(validation_alias='tinyId')
    '''## TinyID'''
    nickname: str = Field(validation_alias='nickName')
    '''## 昵称'''
    head_url: str = Field(validation_alias='headUrl')
    '''## 头像URL'''


class FetchEmojiLike(AliceBotAPIModel):
    '''# 表情回应用户'''
    result: int
    '''## 结果码'''
    error_message: str = Field(validation_alias='errMsg')
    '''## 错误信息'''
    emoji_likes: list[_EmojiLikesList] = Field(validation_alias='isLastPage')
    '''## 回应用户列表'''
    cookie: str
    '''## 下一页游标'''
    is_last_page: bool = Field(validation_alias='isLastPage')
    '''## 是否末页'''
    is_first_page: bool = Field(validation_alias='isFirstPage')
    '''## 是否首页'''


class FetchPttText(AliceBotAPIModel):
    '''# 语音转文字结果'''
    text: str
    '''## 语音转写文本'''


class _AiCharacter(_ChildModel):
    '''# 角色类型'''
    id: str = Field(validation_alias='character_id')
    '''## 角色ID'''
    name: str = Field(validation_alias='character_name')
    '''## 角色名称'''
    preview: str = Field(validation_alias='preview_url')
    '''## 预览URL'''


class AiCharacters(AliceBotAPIModel):
    '''# AI 语音角色'''
    type: str
    '''## 角色类型'''
    characters: list[_AiCharacter]
    '''## 角色类型'''


class Clientkey(AliceBotAPIModel):
    '''# Client Key'''
    client_key: str = Field(validation_alias='clientKey')
    '''## Client Key'''
    expire_time: str = Field(validation_alias='expireTime')
    '''## 过期时间'''
    key_index: str = Field(validation_alias='keyIndex')
    '''## key 索引'''


class Cookies(AliceBotAPIModel):
    '''# 获取 Cookies'''
    cookies: str
    '''## 该域名的 Cookie 字符串'''


class Credentials(AliceBotAPIModel):
    '''# 凭证'''
    cookies: str
    '''## 该域名的 Cookie 字符串'''
    token: int
    '''## CSRF 令牌'''
    csrf_token: int
    '''## CSRF 令牌'''


class CSRFToken(AliceBotAPIModel):
    '''# 获取 CSRF 令牌'''
    token: int
    '''## CSRF 令牌'''


class DoubtFriendsAddRequest(AliceBotAPIModel):
    '''# 可疑好友申请'''
    uid: int
    '''## UID'''
    nick: str
    '''## 昵称'''
    source: str
    '''## 来源'''
    msg: str
    '''## 留言'''
    time: int = Field(validation_alias='reqTime')
    '''## 申请时间'''


class _EmojiLikeList(AliceBotAPIModel):
    '''## 表情回应用户'''
    user_id: int
    '''## 用户 ID'''
    nickname: str = Field(validation_alias='nick_name')
    '''## 昵称'''


class GetEmojiLikes(AliceBotAPIModel):
    '''# 获取表情回应用户'''
    emoji_like_list: list[_EmojiLikeList]
    '''## 表情回应用户列表'''


class EssenceMsg(AliceBotAPIModel):
    '''# 精华消息'''
    group_code: int
    msg_seq: int
    msg_random: int
    sender_uin: int
    sender_nick: str
    sender_time: int
    add_digest_uin: int
    add_digest_nick: str
    add_digest_time: int
    can_be_removed: bool
    disable_forward: bool
    msg_content: list[dict[str, Any]]


class FileInfo(AliceBotAPIModel):
    '''# 文件信息'''
    file: str
    url: str
    '''# 文件链接'''
    file_size: int
    '''# 文件大小'''
    file_name: str
    '''# 文件名'''


class FilesetId(AliceBotAPIModel):
    '''# 文件集 ID'''
    fileset_id: str
    '''## 文件集 ID'''


class FileId(AliceBotAPIModel):
    '''# 文件 ID'''
    file_id: str
    '''## 文件 ID'''


class FilesetFileInfo(AliceBotAPIModel):
    '''## 文件集文件信息'''
    fileset_id: str
    '''## 文件集 ID'''
    file_name: str
    '''## 文件名'''
    orig_name: str
    '''## 源文件名'''
    size: int
    '''## 文件大小'''
    share_url: str
    '''## 分享链接'''
    file_id: str
    '''## 文件 ID'''
    download_url: str
    '''## 下载链接'''


class FilesetInfo(AliceBotAPIModel):
    '''# 文件集信息'''
    fileset_id: str
    '''## 文件集 ID'''
    file_list: list[FilesetFileInfo]
    '''## 文件列表'''


class FileUrl(AliceBotAPIModel):
    '''# 文件链接'''
    url: str
    '''## 文件链接'''


class MessageList(AliceBotAPIModel):
    '''# 消息列表'''
    messages: list[MessageEvent]
    '''## 消息列表'''
    
    @field_validator('messages', mode='before')
    def _(cls, data: list[dict[str, Any]]) -> list[MessageEvent]:
        from Alice.core.bot import AliceBot
        from Alice.plugin import get_core
        
        bot_manager = get_core().bot_manager
        events: list[MessageEvent] = list()
        bot = None
        for raw_event in data:
            group = 'group_id' in raw_event
            self_id = raw_event.get('self_id', 1)
            bot = bot_manager.bots.get(self_id, bot)
            if bot is None:
                bot = AliceBot(-1)
            sent = self_id == raw_event.get('user_id', 2)
            if group:
                events.append(GroupMessageSentEvent(bot=bot, **raw_event) if sent else GroupMessageEvent(bot=bot, **raw_event))
            else:
                events.append(PrivateMessageEvent(bot=bot, **raw_event) if sent else PrivateMessageSentEvent(bot=bot, **raw_event))
        return events


class Friend(AliceBotAPIModel):
    '''# 好友'''
    user_id: int
    '''## QQ 号'''
    nickname: str
    '''## 昵称'''
    remark: str
    '''## 备注名'''


class FriendsCategory(AliceBotAPIModel):
    '''# 好友分组'''
    id: int = Field(validation_alias='categoryId')
    '''## 分组 ID'''
    name: str = Field(validation_alias='categoryName')
    '''## 分组名称'''
    count: int = Field(validation_alias='categoryMbCount')
    '''## 分组好友数'''
    friends: list[Friend] = Field(validation_alias='buddyList')
    '''## 好友列表'''


class Group(AliceBotAPIModel):
    '''# 群聊'''
    group_id: int
    '''## 群号'''
    group_name: str
    '''## 群名称'''
    member_count: int
    '''## 成员数'''
    max_member_count: int
    '''## 最大成员数'''
    level: int = Field(validation_alias='group_level')
    '''## 群等级'''
    create_time: int = Field(validation_alias='group_create_time')
    '''## 创建时间戳'''


class GroupAlbum(AliceBotAPIModel):
    '''# 群相册'''
    id: str
    '''## 相册 ID'''
    title: str
    '''## 相册标题'''
    desc: str
    '''## 简介'''
    coverurl: str
    '''## 封面图片URL'''
    count: int
    '''## 图片数'''
    create_time: str = Field(validation_alias='createtime')
    '''## 创建时间'''
    create_user_id: int = Field(validation_alias='createuin')
    '''## 创建者 QQ 号'''
    create_nickname: str = Field(validation_alias='createnickname')
    '''## 创建者昵称'''
    updatetime: str
    '''## 更新时间'''


class GroupAtAllRemain(AliceBotAPIModel):
    '''# 群 @全体成员 剩余次数'''
    can_at_all: bool
    '''## 当前是否可 @全体成员'''
    count_group: int = Field(validation_alias='remain_at_all_count_for_group')
    '''## 本群今日剩余次数'''
    count_uin: int = Field(validation_alias='remain_at_all_count_for_uin')
    '''## 本账号今日剩余次数'''


class GroupFileSystemInfo(AliceBotAPIModel):
    '''# 群文件系统信息'''
    file_count: int
    '''## 当前文件数'''
    limit_count: int
    '''## 文件数上限'''
    used_space: int
    '''## 已用空间'''
    total_space: int
    '''## 总空间'''


class GroupFile(AliceBotAPIModel):
    '''# 群文件'''
    group_id: int
    '''## 群号'''
    file_id: str
    '''## 群文件 ID'''
    file_name: str
    '''## 群文件名'''
    file_size: int
    '''## 群文件大小'''
    busid: int
    upload_time: int
    '''## 上传时间戳'''
    dead_time: int
    '''## 过期时间戳'''
    modify_time: int
    '''## 修改时间戳'''
    download_times: int
    '''## 下载次数'''
    uploader: int
    '''## 上传者 QQ 号'''
    uploader_name: str
    '''## 上传者昵称'''


class GroupFolder(AliceBotAPIModel):
    '''# 群文件夹'''
    group_id: int
    '''## 群号'''
    folder_id: str
    '''## 群文件夹 ID'''
    folder_name: str
    '''## 群文件夹名'''
    create_time: int
    '''## 创建时间戳'''
    creator: int
    '''## 创建者 QQ 号'''
    create_name: str
    '''## 创建者昵称'''
    count: int = Field(validation_alias='total_file_count')
    '''## 文件数'''


class GroupFilesByFolder(AliceBotAPIModel):
    '''# 群子目录文件列表'''
    files: list[GroupFile]
    '''## 文件列表'''
    folders: list[GroupFolder]
    '''## 文件夹列表'''


class GroupHonor(AliceBotAPIModel):
    '''# 群荣誉'''
    user_id: int
    '''## QQ 号'''
    nickname: str
    '''## 昵称'''
    avatar: str
    '''## 头像URL'''
    description: str
    '''## 荣誉描述'''


class GroupHonorInfo(AliceBotAPIModel):
    '''# 群荣誉信息'''
    group_id: int
    '''## 群号'''
    current_talkative: Optional[GroupHonor]
    '''## 当前龙王'''
    talkative_list: list[GroupHonor]
    '''## 历史龙王'''
    performer_list: list[GroupHonor]
    '''## 群聊之火'''
    legend_list: list[GroupHonor]
    '''## 群聊炽焰'''
    strong_newbie_list: list[GroupHonor]
    '''## 冒尖小春笋'''
    emotion_list: list[GroupHonor]
    '''## 快乐之源'''


class GroupIgnoreAddRequest(AliceBotAPIModel):
    '''# 被忽略的入群请求'''
    group_id: int
    '''## 群号'''
    group_name: str
    '''## 群名称'''
    request_id: int
    '''## 请求序列号'''
    requester_nick: str
    '''## 申请人昵称'''
    message: str
    '''## 验证留言'''
    checked: bool
    '''## 是否已处理'''
    actor: int
    '''## 处理人 QQ 号'''
    invitor_uin: int
    '''## 邀请人 QQ 号'''
    invitor_nick: str
    '''## 邀请人昵称'''


class GroupIgnoreNotifies(AliceBotAPIModel):
    '''# 被忽略的入群请求'''
    group_id: int
    '''## 群号'''
    group_name: str
    '''## 群名称'''
    request_id: int
    '''## 请求序列号'''
    requester_uin: str
    '''## 申请人 QQ 号'''
    requester_nick: str
    '''## 申请人昵称'''
    message: str
    '''## 验证留言'''
    checked: bool
    '''## 是否已处理'''
    actor: int
    '''## 处理人 QQ 号'''
    invitor_uin: int
    '''## 邀请人 QQ 号'''
    invitor_nick: str
    '''## 邀请人昵称'''
    flag: str
    '''## 处理用标记'''


class GroupMember(AliceBotAPIModel):
    '''# 群成员'''
    group_id: int
    '''## 群号'''
    user_id: int
    '''## QQ 号'''
    nickname: str
    '''## 昵称'''
    card: str
    '''## 群名片/备注'''
    sex: str
    '''
    ## 性别
    
    ---
    ### 可能的值
    * male: 男
    * female: 女
    * unknown: 未知
    '''
    age: int
    '''## 年龄'''
    area: str
    '''## 地区'''
    join_time: int
    '''## 加群时间戳'''
    last_sent_time: int
    '''## 最后发言时间戳'''
    level: int
    '''## 成员等级'''
    role: str
    '''
    ## 角色
    
    ---
    可能的值:
    * owner: 群主
    * admin: 管理员
    * member: 群员
    '''
    unfriendly: bool
    '''## 是否不良记录成员'''
    title: str
    '''## 专属头衔'''
    title_expire_time: int
    '''## 专属头衔过期时间戳'''
    card_changeable: bool
    '''## 是否允许修改群名片'''


class GroupShutMember(AliceBotAPIModel):
    '''# 禁言中的群成员'''
    user_id: int
    '''## 用户 ID'''
    nickname: str
    '''## 昵称'''
    time: int = Field(validation_alias='shut_up_time')
    '''## 禁言到期时间戳'''


class GroupSignedMember(AliceBotAPIModel):
    '''# 禁言中的群成员'''
    user_id: int
    '''## 用户 ID'''
    nickname: str = Field(validation_alias='nick')
    '''## 昵称'''
    time: int
    '''## 打卡时间戳'''
    rank: int
    '''## 打卡排名'''


class GroupSystemMessage(AliceBotAPIModel):
    '''# 群系统消息'''
    group_id: int
    '''## 群号'''
    group_name: str
    '''## 群名称'''
    request_id: int
    '''## 请求序列号'''
    requester_uin: str
    '''## 申请人 QQ 号'''
    requester_nick: str
    '''## 申请人昵称'''
    message: str
    '''## 验证留言'''
    checked: bool
    '''## 是否已处理'''
    flag: str
    '''## 处理用标记'''


class LoginInfo(AliceBotAPIModel):
    '''# 登陆信息'''
    user_id: int
    '''## QQ 号'''
    nickname: str
    '''## 昵称'''


class _MiniAppArkConfig(AliceBotAPIModel):
    type: str
    width: int
    height: int
    forward: int
    autoSize: int
    ctime: int
    token: str


class _MiniAppArkData(AliceBotAPIModel):
    ver: str
    prompt: str
    config: _MiniAppArkConfig
    app: str
    view: str
    # meta
    share_origin: int = Field(validation_alias='miniappShareOrigin')
    open_refer: str = Field(validation_alias='miniappOpenRefer')


class MiniAppArk(AliceBotAPIModel):
    '''# 小程序卡片 ark'''
    data: _MiniAppArkData



class StoredMessage(AliceBotAPIModel):
    '''# 存储的消息'''
    time: int
    '''## 时间'''
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
    message_seq: int
    raw_message: str
    '''## 原始消息内容'''
    group_id: Optional[int] = None
    '''## 群号'''
    group_name: Optional[str] = None
    '''## 群名称'''
    user_id: int
    '''## 发送者 QQ 号'''
    sender: Sender
    '''## 发送者'''

    @field_validator('message', mode='before')
    def _(cls, data: Any) -> Message:
        return Message(data)

    # 拓展
    @cached_property
    def at_ids(self) -> list[int]:
        '''## 所有艾特对象'''
        return [int(segment.data['qq']) for segment in self.message.segments if segment.type == 'at']

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


class OnlineClients(AliceBotAPIModel):
    '''# 在线客户端'''
    clients: list[Any]
    '''# 在线客户端'''


class _VoteInfo(AliceBotAPIModel):
    total_count: int
    new_count: int
    new_nearby_count: int
    last_visit_time: int


class _FavoriteInfo(AliceBotAPIModel):
    total_count: int
    last_time: int
    today_count: int


class ProfileLike(AliceBotAPIModel):
    '''# 资料点赞'''
    uid: str
    time: int
    vote: _VoteInfo = Field(validation_alias='voteInfo')
    favorite: _FavoriteInfo = Field(validation_alias='favoriteInfo')


class _GroupAlbum(AliceBotAPIModel):
    album_id: str


class GroupAlbumList(AliceBotAPIModel):
    '''# 资料点赞'''
    album_list: list[_GroupAlbum]
    attach_info: str
    has_more: bool


class _QzoneFeed(AliceBotAPIModel):
    user_id: int = Field(validation_alias='uin')
    '''## QQ 号'''
    nickname: str
    '''## 昵称'''
    time: int
    '''## 时间戳'''
    appid: int
    key: str
    html: str


class QzoneFeeds(AliceBotAPIModel):
    feeds: list[_QzoneFeed]
    has_more: bool



class _QzoneMessage(AliceBotAPIModel):
    tid: str
    '''## 说说 ID'''
    content: str
    '''## 内容'''
    time: int
    '''## 时间戳'''
    comment_num: int
    '''## 评论数'''
    is_private: bool
    '''## 是否仅自己可见'''
    images: list[str]
    '''## 图片'''


class QzoneMessageList(AliceBotAPIModel):
    total: int
    messages: list[_QzoneMessage]


class RecordFileInfo(FileInfo):
    out_format: Optional[str] = None
    base64: Optional[str] = None


class Rkey(AliceBotAPIModel):
    rkey: str
    type: int
    ttl: int
    create_time: int


class RkeyServer(AliceBotAPIModel):
    name: str
    expired_time: int
    '''## 过期时间戳'''
    private_rkey: str
    '''## 私聊 rkey'''
    group_rkey: str
    '''## 群聊 rkey'''


class StrangerInfo(AliceBotAPIModel):
    user_id: int
    '''## QQ 号'''
    nickname: str
    '''## 昵称'''
    sex: str
    '''
    ## 性别
    
    ---
    ### 可能的值
    * male: 男
    * female: 女
    * unknown: 未知
    '''
    age: int
    '''## 年龄'''
    level: int
    '''## QQ 等级'''
    qq_level: int
    '''## QQ 等级'''


class VersionInfo(AliceBotAPIModel):
    '''# 获取版本信息'''
    app_name: str
    '''## 应用标识'''
    app_version: str
    '''## 应用版本'''
    protocol_version: str
    '''## OneBot 标准版本'''


class _OCRPosition(AliceBotAPIModel):
    x: int
    y: int


class _OCRText(AliceBotAPIModel):
    text: str
    '''## 识别文本'''
    confidence: int
    '''## 可信度'''
    coordinates: tuple[_OCRPosition, _OCRPosition, _OCRPosition, _OCRPosition]
    '''## 识别文本'''


class OCR(AliceBotAPIModel):
    '''# OCR 结果'''
    texts: list[_OCRText]
    '''## 识别文本列表'''
    language: str
    '''## 识别语言'''


class DecryptKey(AliceBotAPIModel):
    '''# 数据库解密密钥'''
    db_key: str
    '''## 密钥'''


class ArkShare(AliceBotAPIModel):
    '''# Ark 卡片'''
    ark: str = Field(validation_alias='arkMsg')
    '''## Ark 卡片'''


class SendMessage(AliceBotAPIModel):
    '''# 发送闪传消息'''
    message_id: int


class SendForwardMessage(SendMessage):
    '''# 发送合并转发'''
    res_id: str
    forward_id: str


class SendQzoneMessage(AliceBotAPIModel):
    '''# 发送合并转发'''
    tid: str
    '''## 说说 ID'''
    time: str
    '''## 说说发布时间'''


class QzoneMsgRight(AliceBotAPIModel):
    '''# 说说查看权限'''
    ugc_right: int
    '''## 查看权限'''


class TransGroupFile(AliceBotAPIModel):
    '''# 转存群文件'''
    ok: bool


class TranslateEN2ZH(AliceBotAPIModel):
    '''# 转存群文件'''
    words: list[str]


