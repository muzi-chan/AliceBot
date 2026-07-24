from asyncio import Future, TimeoutError, wait_for
from typing import NoReturn, Optional, TYPE_CHECKING

from Alice.core.plugin.condition import Condition
from Alice.exception import ActionDone, RequireExplicitParam
from Alice.onebot.api import API
from Alice.onebot.event._event import MessageEvent
from Alice.onebot.message import MessageSegment, MessageLike

if TYPE_CHECKING:
    from Alice.core.bot.api import AliceBotAPIResponse
    from Alice.core.bot.bot import AliceBot
    from Alice.core.plugin.trigger import Trigger, TriggerRecord
    from Alice.core.plugin.worker import Tick
    from Alice.onebot.api._model import SendMessage, StoredMessage


class Action:
    
    __slots__ = ('bot', 'tick', 'trigger')
    
    bot: Optional[AliceBot]
    tick: Tick
    trigger: Trigger
    
    def __init__(self, tick: Tick, trigger: Trigger) -> None:
        self.bot = tick.bot
        self.tick = tick
        self.trigger = trigger
    
    async def send(self, message: MessageLike, at_sender: bool = False, bot: Optional[AliceBot] = None, group_id: Optional[int] = None, user_id: Optional[int] = None, timeout: float = 10) -> AliceBotAPIResponse[SendMessage]:
        '''
        ## 发送消息
        
        ---
        ### 参数
        * message: 待发送消息
        * at_sender: 是否@发送者, 仅在群聊中生效
        * bot: 行动主体机器人, 默认解析为事件来源机器人, 如无来源且为 `None` 则抛出异常
        * group_id: 群号, 用于发送群聊消息, 默认解析为事件来源群聊
        * user_id: 用户QQ号, 用于发送私聊消息, 默认解析为事件来源用户
        * timeout: 超时时间
        '''
        bot = bot or self.bot
        if bot is None:
            raise RequireExplicitParam('bot')
        event = self.tick.event
        group_id = getattr(event, 'group_id', None) if group_id is None else group_id
        user_id = getattr(event, 'user_id', None) if user_id is None else user_id
        if at_sender and group_id is not None and user_id is not None:
            message = MessageSegment.at(str(user_id)) + message
        if group_id is not None:
            call = API.send_group_msg(group_id=group_id, message=message)
        elif user_id is not None:
            call = API.send_private_msg(user_id=user_id, message=message)
        else:
            raise RequireExplicitParam('group_id', 'user_id')
        resp = await call(bot, timeout)
        return resp
    
    async def done(self, message: Optional[MessageLike] = None, at_sender:bool = False, bot: Optional[AliceBot] = None, group_id: Optional[int] = None, user_id: Optional[int] = None, timeout: float = 10) -> NoReturn:
        '''
        ## 发送消息并结束当前流程
        
        ---
        ### 参数
        * message: 待发送消息
        * at_sender: 是否@发送者, 仅在群聊中生效
        * bot: 行动主体机器人, 默认解析为事件来源机器人, 如无来源且为 `None` 则抛出异常
        * group_id: 群号, 用于发送群聊消息, 默认解析为事件来源群聊
        * user_id: 用户QQ号, 用于发送私聊消息, 默认解析为事件来源用户
        * timeout: 超时时间
        '''
        if message is not None:
            await self.send(message, at_sender, bot, group_id, user_id, timeout)
        raise ActionDone
    
    async def recv(self, bot: Optional[AliceBot] = None, group_id: Optional[int] = None, user_id: Optional[int] = None, timeout: float = 60) -> Optional[MessageEvent]:
        '''
        ## 接收一条消息
        
        ---
        默认接收当前对话下事件来源用户的下一条消息
        
        ---
        ### 参数
        * bot: 行动主体机器人, 默认解析为事件来源机器人, 如无来源且为 `None` 则抛出异常
        * group_id: 群号
        * user_id: 用户QQ号
        * timeout: 超时时间
        '''
        from Alice.core.plugin.trigger import Trigger
        
        BOT = bot or self.bot
        if BOT is None:
            raise RequireExplicitParam('bot')
        event = self.tick.event
        group_mode = group_id is not None and user_id is None
        group_id = getattr(event, 'group_id', None) if group_id is None else group_id
        user_id = getattr(event, 'user_id', None) if user_id is None else user_id
        desc = '接收来自'
        if group_id is not None:
            desc += f'群[{group_id}]'
        elif user_id is not None:
            desc += f'用户[{user_id}]'
        else:
            raise RequireExplicitParam('group_id', 'user_id')
        desc += '的消息'
        fut: Future[MessageEvent] = Future()
        plugin = self.trigger.plugin
        async def condition(action: Action, tick: Tick, record: TriggerRecord) -> bool:
            bot = action.bot
            if bot is None or bot.account != BOT.account:
                return False
            event = tick.event
            if not isinstance(event, MessageEvent):
                return False
            eq_gid = getattr(event, 'group_id', None) == group_id
            eq_uid = getattr(event, 'user_id', None) == user_id
            if group_mode and eq_gid or eq_gid and eq_uid:
                fut.set_result(event)
                return True
            return False
        trigger = Trigger(Condition(condition, desc), name=desc, plugin=plugin, priority=self.trigger.priority-1)
        try:
            event = await wait_for(fut, timeout)
            return event
        except TimeoutError:
            return
        finally:
            trigger.remove()

    async def get_reply(self, event: MessageEvent) -> Optional[AliceBotAPIResponse[StoredMessage]]:
        '''
        ## 获取回复的消息
        
        ---
        ### 参数
        * event: 消息事件
        '''
        if event.reply_id is None:
            return
        call = API.get_msg(message_id=event.reply_id)
        return await call(event.bot)


__all__ = [
    'Action',
]