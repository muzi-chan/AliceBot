from typing import Literal, Union
from warnings import deprecated

from Alice.core.bot.api import AliceBotAPI
from Alice.onebot.api._model import *
from Alice.onebot.event._model import Status
from Alice.onebot.message import MessageLike


class API:
    
    @AliceBotAPI
    def _del_group_notice(*, group_id: Union[str, int], fid: str = ..., notice_id: str = ...) -> None:
        '''
        ## 删除群公告

        ---
        ### 参数
        * group_id: 群号
        * fid: 公告ID
        * notice_id: 公告ID
        '''
        ...

    @AliceBotAPI
    def _get_group_notice(*, group_id: Union[str, int]) -> None:
        '''
        ## 获取群公告

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def _get_model_show(*, model: str = '') -> list[ModelShow]:
        '''
        ## 获取机型展示

        ---
        ### 参数
        * model: 机型
        '''
        ...

    @AliceBotAPI
    def _mark_all_as_read() -> None:
        '''
        ## 标记全部已读
        '''
        ...

    @AliceBotAPI
    def _send_group_notice(*, group_id: Union[str, int], content: str, image: str = '', pinned: bool = ..., type: Any = ..., confirm_required: bool = ...) -> None:
        '''
        ## 发送群公告

        ---
        ### 参数
        * group_id: 群号
        * content: 公告内容
        * image: 公告图片
            - URI
            - Base64
        * pinned: 是否置顶
        * type
        * confirm_required: 是否需要确认
        '''
        ...

    @AliceBotAPI
    def _set_model_show() -> None:
        '''
        ## 设置机型展示
        '''
        ...

    @AliceBotAPI
    def get_word_slices() -> None:
        '''
        ## 分词
        '''
        ...

    @AliceBotAPI
    def add_custom_face(*, file: str) -> None:
        '''
        ## 添加收藏表情

        ---
        ### 参数
        * file: 表情文件
            - URI
            - Base64
        '''
        ...

    @AliceBotAPI
    def bot_exit() -> None:
        '''
        ## 退出机器人
        '''
        ...

    @AliceBotAPI
    def can_send_image() -> CanSend:
        '''
        ## 是否支持发送图片
        '''
        ...

    @AliceBotAPI
    def can_send_record() -> CanSend:
        '''
        ## 是否支持发送语音
        '''
        ...

    @AliceBotAPI
    def cancel_group_album_media_like(*, group_id: Union[str, int], album_id: str, batch_id: str, lloc: str = ...) -> None:
        '''
        ## 取消点赞群相册媒体

        ---
        ### 参数
        * group_id: 群号
        * album_id: 相册 ID
        * batch_id
        * lloc: 媒体ID
        '''
        ...

    @AliceBotAPI
    def cancel_group_todo(*, group_id: Union[str, int], message_id: Union[str, int]) -> None:
        '''
        ## 取消群待办

        ---
        ### 参数
        * group_id: 群号
        * message_id: 消息 ID
        '''
        ...

    @AliceBotAPI
    def check_url_safely(*, url: str) -> CheckUrlSafely:
        '''
        ## 检查链接安全性

        ---
        ### 参数
        url: 要检查的 URL
        '''
        ...

    @AliceBotAPI
    def clean_cache() -> None:
        '''
        ## 清理缓存
        '''
        ...

    @AliceBotAPI
    def clean_stream_temp_file() -> CleanStreamTempFile:
        '''
        ## 清理流式传输临时文件
        '''
        ...

    @AliceBotAPI
    def click_inline_keyboard_button(*, group_id: Union[str, int], bot_appid: Union[str, int], msg_seq: Union[str, int]) -> None:
        '''
        ## 点击内联键盘按钮

        ---
        ### 参数
        * group_id: 群号
        * bot_appid: 机器人App ID
        * msg_seq: 消息序列号
        '''
        ...

    @AliceBotAPI
    def comment_qzone(*, tid: str, content: str, target_uin: Union[str, int] = ..., images: list[str] = ...) -> None:
        '''
        ## 评论一条说说

        ---
        ### 参数
        * tid: 说说 tid
        * content: 评论内容
        * target_uin: 说说所属 QQ 号, 省略则为机器人自己
        * images: 图片数组
            - URI
            - Base64
        '''
        ...

    @AliceBotAPI
    def complete_group_todo(*, group_id: Union[str, int], message_id: Union[str, int]) -> None:
        '''
        ## 完成群待办

        ---
        ### 参数
        * group_id: 群号
        * message_id: 消息 ID
        '''
        ...

    @AliceBotAPI
    def create_collection() -> None:
        '''
        ## 创建收藏
        '''
        ...

    @AliceBotAPI
    def create_flash_task(*, files: Union[str, list[str]], name: str = ..., thumb_path: str = ...) -> CreateFlashTask:
        '''
        ## 创建闪传任务

        ---
        ### 参数
        * files: 文件列表或单个文件路径
        * name: 任务名称
        * thumb_path: 缩略图路径
        '''
        ...

    @AliceBotAPI
    def create_group_file_folder(*, group_id: Union[str, int], name: str, parent_id: str = '/') -> None:
        '''
        ## 创建群文件夹

        ---
        ### 参数
        * group_id: 群号
        * name: 文件夹名称
        * parent_id: 上级文件夹名称
        '''
        ...

    @AliceBotAPI
    def del_group_album_media(*, group_id: Union[str, int], album_id: str, lloc: str) -> None:
        '''
        ## 删除群相册媒体

        ---
        ### 参数
        * group_id: 群号
        * album_id: 相册 ID
        * lloc: 媒体 ID
        '''
        ...

    @AliceBotAPI
    def delete_custom_face(*, emoji_id: str) -> None:
        '''
        ## 删除收藏表情

        ---
        ### 参数
        * emoji_id: 表情 ID
        '''
        ...

    @AliceBotAPI
    def delete_essence_msg(*, message_id: Union[str, int]) -> None:
        '''
        ## 移除精华消息

        ---
        ### 参数
        * message_id: 消息 ID
        '''
        ...

    @AliceBotAPI
    def delete_flash_file(*, fileset_id: str) -> None:
        '''
        ## 删除闪传文件

        ---
        ### 参数
        * fileset_id: 文件集 ID
        '''
        ...

    @AliceBotAPI
    def delete_friend(*, user_id: Union[str, int], block: Any = False) -> None:
        '''
        ## 删除好友

        ---
        ### 参数
        * user_id: QQ 号
        * block: 是否加入黑名单
        '''
        ...

    @AliceBotAPI
    def delete_group_file(*, group_id: Union[str, int], file_id: str) -> None:
        '''
        ## 删除群文件

        ---
        ### 参数
        * group_id: 群号
        * file_id: 文件 ID
        '''
        ...

    @AliceBotAPI
    def delete_group_file_folder(*, group_id: Union[str, int], folder_id: str) -> None:
        '''
        ## 删除群文件夹

        ---
        ### 参数
        * group_id: 群号
        * folder_id: 文件夹 ID
        '''
        ...

    @AliceBotAPI
    def delete_group_folder(*, group_id: Union[str, int], folder_id: str) -> None:
        '''
        ## 删除群文件夹

        ---
        ### 参数
        * group_id: 群号
        * folder_id: 文件夹 ID
        '''
        ...

    @AliceBotAPI
    def delete_msg(*, message_id: Union[str, int]) -> None:
        '''
        ## 撤回消息

        ---
        ### 参数
        * message_id: 消息 ID
        '''
        ...

    @AliceBotAPI
    def delete_qzone_msg(*, tid: str) -> None:
        '''
        ## 删除一条说说

        ---
        ### 参数
        * tid: 说说 tid
        '''
        ...

    @AliceBotAPI
    def do_group_album_comment(*, group_id: Union[str, int], album_id: str, lloc: str, content: str) -> None:
        '''
        ## 发表群相册评论

        ---
        ### 参数
        * group_id: 群号
        * album_id: 相册 ID
        * lloc: 图片 ID
        * content: 评论内容
        '''
        ...

    @AliceBotAPI
    def download_file(*, url: str = '', base64: str = '', name: str = '') -> DownloadFile:
        '''
        ## 下载文件

        ---
        ### 参数
        * url: 下载链接
        * base64: base64数据
        * name: 文件名
        '''
        ...

    @AliceBotAPI
    def download_fileset(*, fileset_id: str, file_name: str = ..., file_index: float = ...) -> DownloadFileset:
        '''
        ## 解析闪传文件下载直链

        ---
        ### 参数
        * fileset_id: 文件集 ID
        * file_name: 文件名
        * file_index: 文件索引
        '''
        ...

    @AliceBotAPI
    def fetch_custom_face(*, count: int = 10, return_type: str = 'url') -> list[str]:
        '''
        ## 获取自定义表情

        ---
        ### 参数
        * count: 获取数量
        * return_type: `url`时返回`图片URL`, `id`时返回`emoji_id` 
        '''
        ...

    @AliceBotAPI
    def fetch_emoji_like(*, message_id: Union[str, int], emojiId: str, count: int = 10, cookie: str = '') -> FetchEmojiLike:
        '''
        ## 获取表情回应用户

        ---
        ### 参数
        * message_id: 消息 ID
        * emojiId: 表情ID
        * count: 获取数量
        * cookie: 分页Cookie
        '''
        ...

    @AliceBotAPI
    def fetch_ptt_text(*, message_id: str = '') -> FetchPttText:
        '''
        ## 获取语音转文字结果

        ---
        ### 参数
        * message_id: 消息 ID
        '''
        ...

    @AliceBotAPI
    def forward_friend_single_msg(*, message_id: Union[str, int], user_id: Union[str, int]) -> None:
        '''
        ## 转发单条消息给好友

        ---
        ### 参数
        * message_id: 消息 ID
        * user_id: 目标用户QQ
        '''
        ...

    @AliceBotAPI
    def forward_group_single_msg(*, message_id: Union[str, int], group_id: Union[str, int]) -> None:
        '''
        ## 转发单条消息到群

        ---
        ### 参数
        * message_id: 消息 ID
        * group_id: 目标群号
        '''
        ...

    @AliceBotAPI
    def friend_poke(*, user_id: Union[str, int], target_id: Union[str, int] = ...) -> None:
        '''
        ## 好友拍一拍

        ---
        ### 参数
        * user_id: 用户QQ
        * target_id: 目标QQ
        '''
        ...

    @AliceBotAPI
    def get_ai_characters(*, group_id: Union[str, int], chat_type: int = 1) -> list[AiCharacters]:
        '''
        ## 获取 AI 语音角色

        ---
        ### 参数
        * group_id: 群号
        * chat_type: 聊天类型
        '''
        ...

    @AliceBotAPI
    def get_ai_record(*, group_id: Union[str, int], character: str, text: str, chat_type: int = 1) -> str:
        '''
        ## 生成 AI 语音

        ---
        ### 参数
        * group_id: 群号
        * character: 角色ID
        * text: 语音文本内容
        * chat_type: 聊天类型
        '''
        ...

    @AliceBotAPI
    def get_clientkey() -> Clientkey:
        '''
        ## 获取 clientkey
        '''
        ...

    @AliceBotAPI
    def get_collection_list() -> None:
        '''
        ## 获取收藏列表
        '''
        ...

    @AliceBotAPI
    def get_cookies(*, domain: str = 'qun.qq.com') -> Cookies:
        '''
        ## 获取 Cookies

        ---
        ### 参数
        * domain: 需要获取 cookies 的域名
        '''
        ...

    @AliceBotAPI
    def get_credentials(*, domain: str = 'qun.qq.com') -> Credentials:
        '''
        ## 获取凭证

        ---
        ### 参数
        * domain: 需要获取 cookies 的域名
        '''
        ...

    @AliceBotAPI
    def get_csrf_token() -> CSRFToken:
        '''
        ## 获取 CSRF 令牌
        '''
        ...

    @AliceBotAPI
    def get_doubt_friends_add_request(*, count: int = 50) -> list[DoubtFriendsAddRequest]:
        '''
        ## 获取可疑好友申请

        ---
        ### 参数
        * count: 获取数量
        '''
        ...

    @AliceBotAPI
    def get_emoji_likes(*, message_id: Union[str, int], emoji_id: str) -> GetEmojiLikes:
        '''
        ## 获取表情回应用户

        ---
        ### 参数
        * message_id: 消息 ID
        * emoji_id: 表情 ID
        '''
        ...

    @AliceBotAPI
    def get_essence_msg_list(*, group_id: Union[str, int]) -> list[EssenceMsg]:
        '''
        ## 获取精华消息列表

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def get_file(*, file_id: str = '', file: str = '') -> FileInfo:
        '''
        ## 获取文件信息

        ---
        ### 参数
        * file_id: 文件ID
        * file: 文件路径
        '''
        ...

    @AliceBotAPI
    def get_fileset_id(*, share_code: str) -> FilesetId:
        '''
        ## 从分享码/链接获取 fileset_id

        ---
        ### 参数
        * share_code
        '''
        ...

    @AliceBotAPI
    def get_fileset_info(*, fileset_id: str) -> FilesetInfo:
        '''
        ## 获取文件集信息

        ---
        ### 参数
        * fileset_id: 文件集 ID
        '''
        ...

    @AliceBotAPI
    def get_flash_file_list(*, fileset_id: str) -> list[FilesetFileInfo]:
        '''
        ## 获取闪传文件列表

        ---
        ### 参数
        * fileset_id: 文件集 ID
        '''
        ...

    @AliceBotAPI
    def get_flash_file_url(*, fileset_id: str, file_name: str = ..., file_index: float = ...) -> FileUrl:
        '''
        ## 获取闪传文件链接

        ---
        ### 参数
        * fileset_id: 文件集 ID
        * file_name: 文件名
        * file_index: 文件索引
        '''
        ...

    @AliceBotAPI
    def get_forward_msg(*, id: str = ...) -> MessageList:
        '''
        ## 获取合并转发消息

        ---
        ### 参数
        * id: 消息ID
        '''
        ...

    @AliceBotAPI
    def get_friend_list() -> list[Friend]:
        '''
        ## 获取好友列表
        '''
        ...
    
    @AliceBotAPI
    def get_friend_msg_history(*, user_id: Union[str, int], message_id: int = 0, count: int = 20) -> MessageList:
        '''
        ## 获取好友消息历史

        ---
        ### 参数
        * user_id: QQ 号
        * message_id: 消息 ID
        * count
        '''
        ...

    @AliceBotAPI
    def get_friends_with_category() -> list[FriendsCategory]:
        '''
        ## 获取分组好友列表
        '''
        ...

    @AliceBotAPI
    def get_group_album_list(*, group_id: Union[str, int]) -> list[GroupAlbum]:
        '''
        ## get_group_album_list

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    @deprecated('未实现')
    def get_group_album_media_list(*, group_id: Union[str, int], album_id: str, attach_info: str = '') -> None:
        '''
        ## get_group_album_media_list

        ---
        ### 参数
        * group_id: 群号
        * album_id
        * attach_info
        '''
        ...

    @AliceBotAPI
    def get_group_at_all_remain(*, group_id: Union[str, int]) -> GroupAtAllRemain:
        '''
        ## 获取群 @全体成员 剩余次数

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def get_group_detail_info(*, group_id: Union[str, int]) -> Group:
        '''
        ## 获取群详细信息

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def get_group_file_system_info(*, group_id: Union[str, int]) -> GroupFileSystemInfo:
        '''
        ## 获取群文件系统信息

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def get_group_file_url(*, group_id: Union[str, int], file_id: str, busid: Any = ...) -> FileUrl:
        '''
        ## 获取群文件下载直链

        ---
        ### 参数
        * group_id: 群号
        * file_id: 文件 ID
        * busid
        '''
        ...

    @AliceBotAPI
    def get_group_files_by_folder(*, group_id: Union[str, int], folder_id: str = '', folder: str = '') -> GroupFilesByFolder:
        '''
        ## 获取群子目录文件列表

        ---
        ### 参数
        * group_id: 群号
        * folder_id: 文件夹 ID
        * folder: 文件夹
        '''
        ...

    @AliceBotAPI
    def get_group_honor_info(*, group_id: Union[str, int], type: Literal['all', 'talkative', 'performer', 'legend', 'strong_newbie', 'emotion'] = ...) -> GroupHonorInfo:
        '''
        ## 获取群荣誉信息

        ---
        ### 参数
        * group_id: 群号
        * type: 群荣誉类型, `all` `talkative` `performer` `legend` `strong_newbie` `emotion` 
        '''
        ...
    
    @AliceBotAPI
    def get_group_ignore_add_request() -> list[GroupIgnoreAddRequest]:
        '''
        ## 获取被忽略的入群请求
        '''
        ...

    @AliceBotAPI
    def get_group_ignored_notifies() -> list[GroupIgnoreNotifies]:
        '''
        ## 获取被过滤的入群请求
        '''
        ...

    @AliceBotAPI
    def get_group_info(*, group_id: Union[str, int], no_cache: Any = False) -> Group:
        '''
        ## 获取群信息

        ---
        ### 参数
        * group_id: 群号
        * no_cache: 是否不使用缓存
        '''
        ...

    @AliceBotAPI
    def get_group_info_ex(*, group_id: Union[str, int]) -> Group:
        '''
        ## 获取群信息

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def get_group_list(*, no_cache: Any = False) -> list[Group]:
        '''
        ## 获取群列表

        ---
        ### 参数
        * no_cache: 是否不使用缓存
        '''
        ...

    @AliceBotAPI
    def get_group_member_info(*, group_id: Union[str, int], user_id: Union[str, int], no_cache: Any = False) -> GroupMember:
        '''
        ## 获取群成员信息

        ---
        ### 参数
        * group_id: 群号
        * user_id: QQ 号
        * no_cache: 是否不使用缓存
        '''
        ...

    @AliceBotAPI
    def get_group_member_list(*, group_id: Union[str, int], no_cache: Any = False) -> list[GroupMember]:
        '''
        ## 获取群成员列表

        ---
        ### 参数
        * group_id: 群号
        * no_cache: 是否不使用缓存
        '''
        ...

    @AliceBotAPI
    def get_group_msg_history(*, group_id: Union[str, int], message_id: int = 0, count: int = 20) -> list[MessageList]:
        '''
        ## 获取群消息历史

        ---
        ### 参数
        * group_id: 群号
        * message_id: 消息 ID
        * count: 消息数
        '''
        ...

    @AliceBotAPI
    def get_group_root_files(*, group_id: Union[str, int]) -> GroupFilesByFolder:
        '''
        ## 获取群根目录文件列表

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def get_group_shut_list(*, group_id: Union[str, int]) -> list[GroupShutMember]:
        '''
        ## 获取群禁言列表

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def get_group_signed_list(*, group_id: Union[str, int]) -> list[GroupSignedMember]:
        '''
        ## 获取群今日打卡列表

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def get_group_system_msg() -> list[GroupSystemMessage]:
        '''
        ## 获取群系统消息
        '''
        ...

    @AliceBotAPI
    def get_image(*, file: str = '', file_id: str = '') -> FileInfo:
        '''
        ## 获取图片信息

        ---
        ### 参数
        * file
        * file_id: 文件 ID
        '''
        ...

    @AliceBotAPI
    def get_login_info() -> LoginInfo:
        '''
        ## 获取登陆信息
        '''
        ...

    @AliceBotAPI
    def get_mini_app_ark() -> MiniAppArk:
        '''
        ## 获取小程序卡片 ark
        '''
        ...

    @AliceBotAPI
    def get_msg(*, message_id: Union[str, int]) -> StoredMessage:
        '''
        ## 获取消息

        ---
        ### 参数
        * message_id: 消息 ID
        '''
        ...
    
    @AliceBotAPI
    @deprecated('未实现')
    def get_online_clients() -> OnlineClients:
        '''
        ## 获取在线客户端
        '''
        ...

    @AliceBotAPI
    def get_private_file_url(*, user_id: Union[str, int] = ..., file_id: str, file_hash: str = '') -> FileUrl:
        '''
        ## 获取私聊文件下载链接

        ---
        ### 参数
        * user_id: QQ 号
        * file_id: 文件 ID
        * file_hash: 文件哈希值
        '''
        ...

    @AliceBotAPI
    def get_profile_like(*, user_id: int = 0, start: int = 0, count: int = 10) -> ProfileLike:
        '''
        ## 获取资料点赞

        ---
        ### 参数
        * user_id: QQ 号
        * start
        * count
        '''
        ...

    @AliceBotAPI
    def get_qun_album_list(*, group_id: Union[str, int]) -> GroupAlbumList:
        '''
        ## 获取群相册列表

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def get_qzone_feeds(*, page_num: int = 1, count: int = 8) -> QzoneFeeds:
        '''
        ## 获取 QQ 空间好友动态

        ---
        ### 参数
        * page_num: 页码
        * count: 本页数量
        '''
        ...

    @AliceBotAPI
    def get_qzone_msg_list(*, target_uin: Union[str, int] = ..., pos: int = 0, num: int = 20) -> QzoneMessageList:
        '''
        ## 获取 QQ 空间说说列表

        ---
        ### 参数
        * target_uin: 目标 QQ 号, 省略则取机器人自己
        * pos: 起始偏移
        * num: 本页数量
        '''
        ...

    @AliceBotAPI
    @deprecated('未实现')
    def get_recent_contact(*, count: int = 10) -> None:
        '''
        ## 获取最近会话

        ---
        ### 参数
        * count: 数量
        '''
        ...

    @AliceBotAPI
    def get_record(*, out_format: str, file: str = '', file_id: str = '') -> RecordFileInfo:
        '''
        ## 获取语音信息

        ---
        ### 参数
        * file: 文件
        * file_id: 文件 ID
        * out_format: 输出格式
        '''
        ...
    
    @AliceBotAPI
    def get_rkey() -> list[Rkey]:
        '''
        ## 获取下载 rkey
        '''
        ...
    
    @AliceBotAPI
    def get_rkey_server() -> RkeyServer:
        '''
        ## 获取 rkey 服务器信息
        '''
        ...

    @AliceBotAPI
    def get_share_link(*, fileset_id: str) -> str:
        '''
        ## 获取文件分享链接

        ---
        ### 参数
        * fileset_id: 文件集 ID
        '''
        ...

    @AliceBotAPI
    def get_status() -> Status:
        '''
        ## get_status

        ---
        ---
        ### 响应数据
        运行状态。`online`/`good` 均表示账号是否在线。
        '''
        ...

    @AliceBotAPI
    def get_stranger_info(*, user_id: Union[str, int]) -> StrangerInfo:
        '''
        ## 获取陌生人信息

        ---
        ### 参数
        * user_id: QQ 号
        '''
        ...

    @AliceBotAPI
    @deprecated('未实现')
    def get_unidirectional_friend_list() -> None:
        '''
        ## 获取单向好友列表
        '''
        ...

    @AliceBotAPI
    def get_version_info() -> VersionInfo:
        '''
        ## get_version_info
        '''
        ...

    @AliceBotAPI
    def group_poke(*, group_id: Union[str, int], user_id: Union[str, int]) -> None:
        '''
        ## 群拍一拍

        ---
        ### 参数
        * group_id: 群号
        * user_id: QQ 号
        '''
        ...

    @AliceBotAPI
    def like_qzone(*, tid: str, target_uin: Union[str, int] = ..., abstime: int = 0) -> None:
        '''
        ## 给一条说说点赞

        ---
        ### 参数
        * tid: 说说 ID
        * target_uin: 说说所属 QQ 号, 省略则为机器人自己
        * abstime: 说说发表时间
        '''
        ...

    @AliceBotAPI
    def list_filesets() -> list[FilesetFileInfo]:
        '''
        ## 列出当前账号的所有闪传文件集
        '''
        ...

    @AliceBotAPI
    def mark_private_msg_as_read(*, message_id: Union[str, int], user_id: Union[str, int] = ...) -> None:
        '''
        ## 标记私聊消息已读

        ---
        ### 参数
        * message_id: 消息 ID
        * user_id: QQ 号
        '''
        ...

    @AliceBotAPI
    def mark_group_msg_as_read(*, message_id: Union[str, int], group_id: Union[str, int] = ...) -> None:
        '''
        ## 标记群消息已读

        ---
        ### 参数
        * message_id: 消息 ID
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def mark_msg_as_read(*, message_id: Union[str, int], target_id: Union[str, int] = ...) -> None:
        '''
        ## 标记消息已读

        ---
        ### 参数
        * message_id: 消息 ID
        * target_id: QQ 号/群号
        '''
        ...

    @AliceBotAPI
    def modify_custom_face(*, emoji_id: str, desc: str = '') -> None:
        '''
        ## 修改收藏表情备注

        ---
        ### 参数
        * emoji_id: 表情 ID
        * desc: 表情描述
        '''
        ...

    @AliceBotAPI
    def move_custom_face_to_front(*, emoji_id: str) -> None:
        '''
        ## 收藏表情移到最前

        ---
        ### 参数
        * emoji_id: 表情 ID
        '''
        ...

    @AliceBotAPI
    def move_group_file(*, group_id: Union[str, int], file_id: str, parent_directory: str, target_directory: str) -> None:
        '''
        ## 移动群文件

        ---
        ### 参数
        * group_id: 群号
        * file_id: 文件 ID
        * parent_directory
        * target_directory
        '''
        ...

    @AliceBotAPI
    @deprecated('仅占位')
    def nc_get_packet_status() -> None:
        '''
        ## 获取 packet 状态

        ---
        ---
        ### 响应数据
        占位实现, 恒返回 null。
        '''
        ...

    @AliceBotAPI
    @deprecated('仅占位')
    def nc_get_user_status(*, user_id: Union[str, int]) -> None:
        '''
        ## 获取用户在线/扩展状态

        ---
        ### 参数
        * user_id: QQ 号
        '''
        ...

    @AliceBotAPI
    def ocr_image(*, image: str) -> OCR:
        '''
        ## OCR 图片

        ---
        ### 参数
        * image: 图片 URL 或 ID
        '''
        ...

    @AliceBotAPI
    def rename_flash_file(*, fileset_id: str, new_name: str) -> None:
        '''
        ## 重命名闪传文件

        ---
        ### 参数
        * fileset_id: 文件集 ID
        * new_name: 新文件名
        '''
        ...

    @AliceBotAPI
    def rename_group_file(*, group_id: Union[str, int], file_id: str, current_parent_directory: str = '/', new_name: str) -> None:
        '''
        ## 重命名群文件

        ---
        ### 参数
        * group_id: 群号
        * file_id: 文件 ID
        * current_parent_directory
        * new_name: 新文件名
        '''
        ...

    @AliceBotAPI
    def rename_group_file_folder(*, group_id: Union[str, int], folder_id: str, new_folder_name: str = '', name: str = '') -> None:
        '''
        ## 重命名群文件夹

        ---
        ### 参数
        * group_id: 群号
        * folder_id: 文件夹 ID
        * new_folder_name: 新文件夹名
        * name
        '''
        ...

    @AliceBotAPI
    def request_decrypt_key(*, db_path: str) -> DecryptKey:
        '''
        ## 请求数据库解密密钥

        ---
        ### 参数
        * db_path: 数据库路径
        '''
        ...

    @AliceBotAPI
    def send_ark_share(*, user_id: Union[str, int] = ..., group_id: Union[str, int] = ..., phone_number: str = '') -> ArkShare:
        '''
        ## 分享用户/群 Ark 卡片

        ---
        ### 参数
        * user_id: QQ 号
        * group_id: 群号
        * phone_number: 手机号
        '''
        ...

    @AliceBotAPI
    def send_flash_msg(*, fileset_id: str, user_id: Union[str, int] = ..., group_id: Union[str, int] = ...) -> SendMessage:
        '''
        ## 发送闪传消息

        ---
        ### 参数
        * fileset_id
        * user_id: QQ 号
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def send_forward_msg(*, user_id: Union[str, int] = ..., group_id: Union[str, int] = ..., messages: MessageLike = ..., message: MessageLike = ...) -> SendForwardMessage:
        '''
        ## 发送合并转发

        ---
        ### 参数
        * group_id: 群号
        * user_id: QQ 号
        * messages: 合并消息
        * message: 合并消息
        '''
        ...

    @AliceBotAPI
    def send_group_ai_record(*, group_id: Union[str, int], character: str, text: str, chat_type: int = 1) -> SendMessage:
        '''
        ## 发送 AI 语音到群

        ---
        ### 参数
        * group_id: 群号
        * character: 角色 ID
        * text: 文本
        * chat_type
        '''
        ...

    @AliceBotAPI
    def send_group_ark_share(*, group_id: Union[str, int]) -> str:
        '''
        ## 分享群 Ark 卡片

        ---
        ### 参数
        * group_id: 群号
        ---
        ### 响应数据
        服务端生成的群推荐 Ark 卡片 JSON 字符串
        '''
        ...

    @AliceBotAPI
    def send_group_forward_msg(*, group_id: Union[str, int], messages: MessageLike = ..., message: MessageLike = ...) -> SendForwardMessage:
        '''
        ## 发送群合并转发

        ---
        ### 参数
        * group_id: 群号
        * messages: 合并消息
        * message: 合并消息
        '''
        ...


    @AliceBotAPI
    def send_group_msg(*, group_id: Union[str, int], message: MessageLike, auto_escape: Any = False) -> SendMessage:
        '''
        ## 发送群消息

        ---
        ### 参数
        * group_id: 群号
        * message: 要发送的消息
        * auto_escape: 消息内容是否作为纯文本发送(即不解析 CQ 码), 只在 `message` 字段是字符串时有效
        '''
        ...

    @AliceBotAPI
    def send_like(*, user_id: Union[str, int], times: int = 1) -> None:
        '''
        ## 点赞

        ---
        ### 参数
        * user_id: QQ 号
        * times: 点赞次数
        '''
        ...

    @AliceBotAPI
    def send_msg(*, message: MessageLike, message_type: Literal['private', 'group'] = ..., group_id: Union[str, int] = ..., user_id: Union[str, int] = ..., auto_escape: Any = False) -> SendMessage:
        '''
        ## 发送消息（按 message_type/群号 自动路由群聊或私聊）

        ---
        ### 参数
        * message: 要发送的消息
        * message_type: 消息类型,支持 `private` `group` 分别对应私聊, 群组, 讨论组, 如不传入, 则根据传入的 `*_id` 参数判断
        * group_id: 群号
        * user_id: QQ 号
        * auto_escape: 消息内容是否作为纯文本发送(即不解析 CQ 码), 只在 `message` 字段是字符串时有效
        '''
        ...

    @AliceBotAPI
    @deprecated('未实现')
    def send_packet(*, cmd: str, data: str = '', rsp: Any = True) -> None:
        '''
        ## 发送原始 SSO 包

        ---
        ### 参数
        * cmd
        * data
        * rsp
        '''
        ...

    @AliceBotAPI
    def send_poke(*, user_id: Union[str, int], group_id: Union[str, int] = ...) -> None:
        '''
        ## 拍一拍

        ---
        ### 参数
        * user_id: QQ 号
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def send_private_forward_msg(*, user_id: Union[str, int], messages: MessageLike = ..., message: MessageLike = ...) -> SendForwardMessage:
        '''
        ## 发送私聊合并转发

        ---
        ### 参数
        * group_id: 群号
        * user_id: QQ 号
        * messages: 合并消息
        * message: 合并消息
        '''
        ...

    @AliceBotAPI
    def send_private_msg(*, user_id: Union[str, int], message: MessageLike, auto_escape: Any = False) -> SendMessage:
        '''
        ## 发送私聊消息

        ---
        ### 参数
        * message: 要发送的消息
        * user_id: QQ 号
        * auto_escape: 消息内容是否作为纯文本发送(即不解析 CQ 码), 只在 `message` 字段是字符串时有效
        '''
        ...

    @AliceBotAPI
    def send_qzone_msg(*, content: str, images: list[str] = ..., ugc_right: Literal[1, 4, 16, 64, 128] = 1, target_uins: list[int] = ...) -> SendQzoneMessage:
        '''
        ## 发表说说

        ---
        ### 参数
        * content: 说说正文
        * images: 图片数组
        * ugc_right: 查看权限 `1`所有人可见 `4`好友可见 `16`部分好友可见 `64`仅自己可见 `128`部分好友不可见
        * target_uins: 权限作用 QQ 号数组 ugc_right=16 时表示可见名单, 128 时表示不可见名单
        '''
        ...

    @AliceBotAPI
    def set_diy_online_status(*, face_id: int, face_type: int = 1, wording: str = '') -> None:
        '''
        ## 设置自定义在线状态

        ---
        ### 参数
        * face_id: 表情 ID
        * face_type: 表情类型
        * wording: 在线状态文本
        '''
        ...

    @AliceBotAPI
    def set_doubt_friends_add_request(*, flag: str, approve: Any = True) -> None:
        '''
        ## 处理可疑好友申请

        ---
        ### 参数
        * flag
        * approve: 同意
        '''
        ...

    @AliceBotAPI
    def set_essence_msg(*, message_id: Union[str, int]) -> None:
        '''
        ## 设置精华消息

        ---
        ### 参数
        * message_id: 消息 ID
        '''
        ...

    @AliceBotAPI
    def set_friend_add_request(*, flag: str, approve: Any = True) -> None:
        '''
        ## 处理好友添加请求

        ---
        ### 参数
        * flag
        * approve: 同意
        '''
        ...

    @AliceBotAPI
    def set_friend_remark(*, user_id: Union[str, int], remark: str) -> None:
        '''
        ## 设置好友备注

        ---
        ### 参数
        * user_id: QQ 号
        * remark: 好友备注
        '''
        ...

    @AliceBotAPI
    def set_group_add_option(*, group_id: Union[str, int], add_type: int = 0) -> None:
        '''
        ## 设置加群选项

        ---
        ### 参数
        * group_id: 群号
        * add_type
        '''
        ...

    @AliceBotAPI
    def set_group_add_request(*, flag: str, sub_type: Any = ..., type: Any = ..., approve: Any = True, reason: str = '') -> None:
        '''
        ## 处理加群请求

        ---
        ### 参数
        * flag
        * sub_type
        * type
        * approve: 同意
        * reason: 原因
        '''
        ...

    @AliceBotAPI
    def set_group_admin(*, group_id: Union[str, int], user_id: Union[str, int], enable: Any = True) -> None:
        '''
        ## 设置/取消管理员

        ---
        ### 参数
        * group_id: 群号
        * user_id: QQ 号
        * enable
        '''
        ...

    @AliceBotAPI
    def set_group_album_media_like(*, group_id: Union[str, int], album_id: str, batch_id: str, lloc: str = ...) -> None:
        '''
        ## 点赞群相册图片

        ---
        ### 参数
        * group_id: 群号
        * album_id: 相册 ID
        * batch_id
        * lloc: 图片 ID
        '''
        ...

    @AliceBotAPI
    @deprecated('未实现')
    def set_group_anonymous() -> None:
        '''
        ## 匿名开关
        '''
        ...

    @AliceBotAPI
    @deprecated('未实现')
    def set_group_anonymous_ban() -> None:
        '''
        ## 匿名禁言
        '''
        ...

    @AliceBotAPI
    def set_group_ban(*, group_id: Union[str, int], user_id: Union[str, int], duration: int = 1800) -> None:
        '''
        ## 禁言群成员

        ---
        ### 参数
        * group_id: 群号
        * user_id: QQ 号
        * duration: 禁言时间(s) 为`0`时解除
        '''
        ...

    @AliceBotAPI
    def set_group_card(*, group_id: Union[str, int], user_id: Union[str, int], card: str = '') -> None:
        '''
        ## 设置群名片

        ---
        ### 参数
        * group_id: 群号
        * user_id: QQ 号
        * card: 群名片 `空字符串清除`
        '''
        ...

    @AliceBotAPI
    def set_group_kick(*, group_id: Union[str, int], user_id: Union[str, int], reject_add_request: Any = False) -> None:
        '''
        ## 踢出群成员

        ---
        ### 参数
        * group_id: 群号
        * user_id: QQ 号
        * reject_add_request: 同时拒绝加群请求
        '''
        ...

    @AliceBotAPI
    def set_group_kick_members(*, group_id: Union[str, int], user_id: list[Union[str, int]], reject_add_request: Any = False) -> None:
        '''
        ## 批量踢出群成员

        ---
        ### 参数
        * group_id: 群号
        * user_id: QQ 号
        * reject_add_request: 同时拒绝加群请求
        '''
        ...

    @AliceBotAPI
    def set_group_leave(*, group_id: Union[str, int]) -> None:
        '''
        ## 退群

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def set_group_name(*, group_id: Union[str, int], group_name: str = '') -> None:
        '''
        ## 设置群名

        ---
        ### 参数
        * group_id: 群号
        * group_name: 群名
        '''
        ...

    @AliceBotAPI
    def set_group_portrait(*, group_id: Union[str, int], file: str) -> None:
        '''
        ## 设置群头像

        ---
        ### 参数
        * group_id: 群号
        * file: 群头像
        '''
        ...

    @AliceBotAPI
    def set_group_reaction(*, group_id: Union[str, int] = ..., message_id: Union[str, int], code: str, is_set: Any = True) -> None:
        '''
        ## 群聊表情回应

        ---
        ### 参数
        * group_id: 群号
        * message_id: 消息 ID
        * code
        * is_set
        '''
        ...

    @AliceBotAPI
    def set_group_remark(*, group_id: Union[str, int], remark: str) -> None:
        '''
        ## 设置群备注

        ---
        ### 参数
        * group_id: 群号
        * remark: 群备注
        '''
        ...

    @AliceBotAPI
    def set_group_robot_add_option(*, group_id: Union[str, int], robot_member_switch: int = ..., robot_member_examine: int = ...) -> None:
        '''
        ## 设置群机器人加群选项

        ---
        ### 参数
        * group_id: 群号
        * robot_member_switch
        * robot_member_examine
        '''
        ...

    @AliceBotAPI
    def set_group_search(*, group_id: Union[str, int], no_finger_open: int = ..., no_code_finger_open: int = ...) -> None:
        '''
        ## 设置群被搜索方式

        ---
        ### 参数
        * group_id: 群号
        * no_finger_open
        * no_code_finger_open
        '''
        ...

    @AliceBotAPI
    def set_group_sign(*, group_id: Union[str, int]) -> None:
        '''
        ## 群签到

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def set_group_special_title(*, group_id: Union[str, int], user_id: Union[str, int], special_title: str = '') -> None:
        '''
        ## 设置群头衔

        ---
        ### 参数
        * group_id: 群号
        * user_id: QQ 号
        * special_title: 群头衔
        '''
        ...

    @AliceBotAPI
    def set_group_todo(*, group_id: Union[str, int], message_id: Union[str, int]) -> None:
        '''
        ## 设置群待办

        ---
        ### 参数
        * group_id: 群号
        * message_id: 消息 ID
        '''
        ...

    @AliceBotAPI
    def set_group_whole_ban(*, group_id: Union[str, int], enable: Any = True) -> None:
        '''
        ## 全员禁言开关

        ---
        ### 参数
        * group_id: 群号
        * enable
        '''
        ...

    @AliceBotAPI
    def set_input_status(*, user_id: Union[str, int], event_type: int = 0) -> None:
        '''
        ## 设置输入状态

        ---
        ### 参数
        * user_id: QQ 号
        * event_type
        '''
        ...

    @AliceBotAPI
    def set_msg_emoji_like(*, message_id: Union[str, int], emoji_id: str, set: Any = True) -> None:
        '''
        ## 设置消息表情回应

        ---
        ### 参数
        * message_id: 消息 ID
        * emoji_id: 表情 ID
        * set: 设置
        '''
        ...

    @AliceBotAPI
    def set_online_status(*, status: int, ext_status: int = 0, battery_status: int = 100) -> None:
        '''
        ## 设置在线状态

        ---
        ### 参数
        * status
        * ext_status
        * battery_status
        '''
        ...

    @AliceBotAPI
    def set_qq_avatar(*, file: str) -> None:
        '''
        ## 设置 QQ 头像

        ---
        ### 参数
        * file: 头像
        '''
        ...

    @AliceBotAPI
    def set_qq_profile(*, nickname: str = ..., personal_note: str = ...) -> None:
        '''
        ## 设置 QQ 资料

        ---
        ### 参数
        * nickname: 昵称
        * personal_note: 个人签名
        '''
        ...

    @AliceBotAPI
    def set_qzone_ban(*, user_id: Union[str, int], enable: Any = True) -> None:
        '''
        ## 拉黑或解除拉黑某人

        ---
        ### 参数
        * user_id: 目标 QQ 号
        * enable: true 拉黑, false 解除拉黑
        '''
        ...

    @AliceBotAPI
    def set_qzone_msg_right(*, tid: str, ugc_right: int, target_uins: Any = ...) -> QzoneMsgRight:
        '''
        ## 修改一条已发说说的查看权限

        ---
        ### 参数
        * tid: 说说 ID
        * ugc_right: 查看权限 `1`所有人可见 `4`好友可见 `16`部分好友可见 `64`仅自己可见 `128`部分好友不可见
        * target_uins: 权限作用 QQ 号数组 ugc_right=16 时表示可见名单, 128 时表示不可见名单
        '''
        ...

    @AliceBotAPI
    @deprecated('未实现')
    def set_restart() -> None:
        '''
        ## 重启
        '''
        ...

    @AliceBotAPI
    def set_self_longnick(*, longNick: str = ..., long_nick: str = ...) -> None:
        '''
        ## 设置个性签名

        ---
        ### 参数
        * longNick: 个性签名
        * long_nick: 个性签名
        '''
        ...

    @AliceBotAPI
    def share_group_ex(*, group_id: Union[str, int]) -> str:
        '''
        ## 分享群 Ark 卡片

        ---
        ### 参数
        * group_id: 群号
        '''
        ...

    @AliceBotAPI
    def share_peer(*, user_id: Union[str, int] = ..., group_id: Union[str, int] = ..., phone_number: str = '') -> ArkShare:
        '''
        ## 分享用户/群 Ark 卡片

        ---
        ### 参数
        * user_id: QQ 号
        * group_id: 群号
        * phone_number: 手机号
        '''
        ...

    @AliceBotAPI
    def trans_group_file(*, group_id: Union[str, int], file_id: str) -> TransGroupFile:
        '''
        ## 转存群文件

        ---
        ### 参数
        * group_id: 群号
        * file_id: 文件 ID
        '''
        ...

    @AliceBotAPI
    def translate_en2zh(*, words: list[str] = ...) -> TranslateEN2ZH:
        '''
        ## 英译中

        ---
        ### 参数
        * words: 待翻译内容
        '''
        ...

    @AliceBotAPI
    def unlike_qzone(*, tid: str, target_uin: Union[str, int] = ..., abstime: int = 0) -> None:
        '''
        ## 取消对一条说说的点赞

        ---
        ### 参数
        * tid: 说说 ID
        * target_uin: 说说所属 QQ 号, 省略则为机器人自己
        * abstime: 说说发表时间
        '''
        ...

    @AliceBotAPI
    def upload_forward_msg(*, messages: MessageLike = ..., message: MessageLike = ..., group_id: Union[str, int] = ...) -> SendForwardMessage:
        '''
        ## 上传转发消息

        ---
        ### 参数
        * group_id: 群号
        * messages: 合并消息
        * message: 合并消息
        '''
        ...

    @AliceBotAPI
    def upload_group_file(*, group_id: Union[str, int], file: str, name: str = '', folder: str = '', folder_id: str = '', upload_file: Any = True) -> FileId:
        '''
        ## 上传群文件

        ---
        ### 参数
        * group_id: 群号
        * file: 文件
        * name: 文件名
        * folder: 文件夹
        * folder_id: 文件夹 ID
        * upload_file
        '''
        ...

    @AliceBotAPI
    def upload_image_to_qun_album(*, group_id: Union[str, int], album_id: str, album_name: str, file: str) -> None:
        '''
        ## 上传图片至群相册

        ---
        ### 参数
        * group_id: 群号
        * album_id: 相册 ID
        * album_name: 群相册名
        * file: 图片
        '''
        ...

    @AliceBotAPI
    def upload_private_file(*, user_id: Union[str, int], file: str, name: str = '', upload_file: Any = True) -> FileId:
        '''
        ## 上传私聊文件

        ---
        ### 参数
        * user_id: QQ 号
        * file: 文件
        * name: 文件名
        * upload_file
        '''
        ...


__all__ = [
    'API',
]