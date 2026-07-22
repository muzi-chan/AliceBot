from typing import Optional

from Alice.core.bot.api import AliceBotAPIModel


class File(AliceBotAPIModel):
    '''# 文件信息'''
    id: str
    '''## 文件 ID'''
    name: str
    '''## 文件名'''
    size: int
    '''## 文件大小'''
    busid: int
    '''## busid'''


class Status(AliceBotAPIModel):
    '''# 状态'''
    online: bool
    '''## 当前 QQ 在线'''
    good: bool
    '''## 状态符合预期'''


class Sender(AliceBotAPIModel):
    '''# 发送者'''
    user_id: int
    '''## 发送者 QQ 号'''
    nickname: Optional[str] = None
    '''## 昵称'''
    card: Optional[str] = None
    '''## 群名片'''
    sex: Optional[str] = None
    '''
    ## 性别
    
    ---
    ### 可能的值
    * male: 男
    * female: 女
    * unknown: 未知
    '''
    age: Optional[int] = None
    '''## 年龄'''
    area: Optional[str] = None
    '''## 地区'''
    level: Optional[str] = None
    '''## 成员等级'''
    role: Optional[str] = None
    '''
    ## 角色
    
    ---
    可能的值:
    * owner: 群主
    * admin: 管理员
    * member: 群员
    '''
    title: Optional[str] = None
    '''## 专属头衔'''


class MsgEmojiLike(AliceBotAPIModel):
    '''# 表情回应'''
    emoji_id: str
    '''## 表情 ID'''
    count: int
    '''## 回应数量'''


