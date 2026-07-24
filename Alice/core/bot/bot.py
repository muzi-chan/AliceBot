import json

from pathlib import Path
from time import time
from typing import Any, Optional, TYPE_CHECKING

from Alice.log import logger

if TYPE_CHECKING:
    from Alice.core.bot.api import AliceBotAPICall, AliceBotAPIResponse, P, R
    from Alice.core.bot.thread import AliceBotWebSocketServerThread


class AliceBotFeiend:
    '''## Alice机器人好友'''
    __slots__ = ('user_id', 'nickname', 'remark')

    user_id: int
    '''## QQ 号'''
    nickname: str
    '''## 昵称'''
    remark: str
    '''## 备注名'''

    def __init__(self, user_id: int, nickname: str, remark: str) -> None:
        self.user_id = user_id
        self.nickname = nickname
        self.remark = remark


class AliceBotGroup:
    '''## Alice机器人群'''
    __slots__ = ('group_id', 'group_name', 'owner', 'admin')

    group_id: int
    '''## 群号'''
    group_name: str
    '''## 群名称'''
    owner: int
    '''## 群主 QQ号'''
    admin: list[int]
    '''## 管理员 QQ号'''
    def __init__(self, group_id: int, group_name: str, owner: int, admin: list[int]) -> None:
        self.group_id = group_id
        self.group_name = group_name
        self.owner = owner
        self.admin = admin


class AliceBotData:
    '''# Alice机器人账号数据类'''
    __slots__ = ('_bot', '_last_update_time', '_admin_groups', '_owned_groups', '_groups', '_friends', '_path', 'nicknames', 'superusers')
    
    _bot: AliceBot
    _last_update_time: float
    _admin_groups: list[int]
    _owned_groups: list[int]
    _groups: dict[int, AliceBotGroup]
    _friends: dict[int, AliceBotFeiend]
    _path: Path
    nicknames: list[str]
    superusers: list[int]
    
    def __init__(self, bot: AliceBot) -> None:
        from Alice.plugin import get_core
        
        self._bot = bot
        self._last_update_time = -1
        self._admin_groups = list()
        self._owned_groups = list()
        self._groups = dict()
        self._friends = dict()
        self._path = get_core().path.bots / f'{self._bot.account}'
        self.nicknames = list()
        self.superusers = list()
    
    @property
    def last_update_time(self) -> float:
        return self._last_update_time
    
    @property
    def admin_groups(self) -> list[int]:
        return self._admin_groups.copy()
    
    @property
    def owned_groups(self) -> list[int]:
        return self._owned_groups.copy()
    
    @property
    def groups(self) -> dict[int, AliceBotGroup]:
        return self._groups.copy()
    
    @property
    def friends(self) -> dict[int, AliceBotFeiend]:
        return self._friends.copy()
    
    @property
    def save_path(self) -> Path:
        return self._path
    
    def load(self) -> None:
        data_path = self._path / 'data.json'
        if not data_path.exists():
            return
        try:
            raw_data = data_path.read_text(encoding='UTF-8')
            data: dict[str, Any] = json.loads(raw_data)
            groups: list[dict[str, Any]] = data.get('groups', list())
            friends: list[dict[str, Any]] = data.get('friends', list())
            nicknames: list[str] = data.get('nicknames', list())
            superusers: list[int] = data.get('superusers', list())
            last_update_time = data['last_update_time']
            if self._last_update_time > last_update_time:
                return
            self._last_update_time = last_update_time
            self._admin_groups = data['admin_groups']
            self._owned_groups = data['owned_groups']
            self._groups = {group['group_id']: AliceBotGroup(**group) for group in groups}
            self._friends = {friend['user_id']: AliceBotFeiend(**friend) for friend in friends}
            self.nicknames = nicknames
            self.superusers = superusers
        except:
            logger.error(f'加载[{self._bot.account}]数据失败')
    
    def save(self) -> None:
        if self._bot.connected and not self._path.exists():
            self._path.mkdir(parents=True, exist_ok=True)
        try:
            groups: list[dict[str, Any]] = [{'group_id': group.group_id, 'group_name': group.group_name, 'owner': group.owner, 'admin': group.admin} for group in self.groups.values()]
            friends: list[dict[str, Any]] = [{'user_id': friend.user_id, 'nickname': friend.nickname, 'remark': friend.remark} for friend in self.friends.values()]
            data: dict[str, Any] = {
                'last_update_time': self.last_update_time,
                'admin_groups': self.admin_groups,
                'owned_groups': self.owned_groups,
                'groups': groups,
                'friends': friends,
                'nicknames': self.nicknames,
                'superusers': self.superusers,
            }
            (self._path / 'data.json').write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding='UTF-8')
        except:
            logger.error(f'保存[{self._bot.account}]数据失败')
    
    async def update(self) -> None:
        if not self._bot.connected:
            return
        from Alice.onebot.api import API
        
        try:
            call_group_list = API.get_group_list()
            resp_group_list = await call_group_list(self._bot)
            admin_groups: list[int] = list()
            owned_groups: list[int] = list()
            for group in resp_group_list.content:
                call_member_list = API.get_group_member_list(group_id=group.group_id)
                resp_member_list = await call_member_list(self._bot)
                owner = next((member.user_id for member in resp_member_list.content if member.role == 'owner'))
                admin = [member.user_id for member in resp_member_list.content if member.role == 'admin']
                self._groups[group.group_id] = AliceBotGroup(group.group_id, group.group_name, owner, admin)
                if self._bot.account in admin:
                    admin_groups.append(group.group_id)
                if self._bot.account == owner:
                    owned_groups.append(group.group_id)
            self._admin_groups = admin_groups
            self._owned_groups = owned_groups
        except:
            logger.error(f'更新[{self._bot.account}]群组数据失败')
        try:
            call_friend_list = API.get_friend_list()
            resp_friend_list = await call_friend_list(self._bot)
            for friend in resp_friend_list.content:
                self._friends[friend.user_id] = AliceBotFeiend(friend.user_id, friend.nickname, friend.remark)
        except:
            logger.error(f'更新[{self._bot.account}]好友数据失败')
        self._last_update_time = time()
        self.save()


class AliceBot:
    '''# Alice机器人类'''
    __slots__ = ('_server', 'account', 'data')

    _server: Optional[AliceBotWebSocketServerThread]
    account: int
    '''## 账号'''
    if TYPE_CHECKING:
        from enum import Enum
        
        class data(Enum):
            '''## 账号数据'''
            last_update_time: float
            '''## 上次更新时间戳'''
            admin_groups: list[int]
            '''## 作为管理员的群'''
            owned_groups: list[int]
            '''## 作为群主的群'''
            groups: dict[int, AliceBotGroup]
            '''## 群组列表'''
            friends: dict[int, AliceBotFeiend]
            '''## 好友列表'''
            path: Path
            '''## 数据目录'''
            nicknames: list[str]
            '''## 昵称'''
            superusers: list[int]
            '''## 超级用户'''
            @staticmethod
            def load() -> None:
                '''## 加载数据'''
            @staticmethod
            def save() -> None:
                '''## 保存数据'''
            @staticmethod
            async def update() -> None:
                '''## 更新数据'''
    
    def __init__(self, account: int) -> None:
        self._server = None
        self.account = account
        self.data = AliceBotData(self) # type: ignore
    
    @property
    def server(self) -> Optional[AliceBotWebSocketServerThread]:
        '''## 所属服务器线程'''
        return self._server
    
    @property
    def connected(self) -> bool:
        '''## 已连接'''
        return self._server is not None
    
    def delete(self, include_data: bool) -> None:
        '''
        ## 从机器人管理器移除自身
        
        ---
        ### 参数
        * include_data: 包括机器人数据, 为 `True` 时将会删除自身的数据目录
        '''
        from Alice.plugin import get_core
        
        get_core().bot_manager._remove_bot(self) # type: ignore
        if include_data and self.data.path.exists():
            from shutil import rmtree
            
            rmtree(self.data.path)
        
    
    async def call(self, call: AliceBotAPICall[P, R], timeout: float = 10) -> AliceBotAPIResponse[R]:
        '''## 调用API对象'''
        return await call(self, timeout)


__all__ = [
    'AliceBot',
]