from json import loads as json_loads
from json import JSONEncoder
from re import finditer as re_finditer

from base64 import b64encode
from io import BytesIO
from pathlib import Path
from typing import Any, Generator, Optional, Self, Union, overload

from PIL.Image import Image


def _escape(v: Any) -> Any:
    if isinstance(v, str):
        v = v.replace('&', '&amp;').replace(',', '&#44;').replace('[', '&#91;').replace(']', '&#93;')
    return v

class MessageSegment:
    '''# 消息段'''
    
    __slots__ = ('type', 'data')
    
    data: dict[str, Any]

    def __init__(self, type: str, data: dict[str, Any]) -> None:
        self.type = type
        if self.type == 'json':
            if raw_data := data.get('data', None):
                self.data = json_loads(raw_data)
            else:
                self.data = {k: _escape(v) for k, v in data.items()}
        else:
            self.data = {k: _escape(v) for k, v in data.items()}
    
    def __str__(self) -> str:
        return str(self.cqcode)

    def __repr__(self) -> str:
        return f'MessageSegment(type={self.type}, data={self.data})'

    def __add__(self, other: MessageLike) -> Message:
        message = Message(self)
        return message + other

    def __radd__(self, other: MessageLike) -> Message:
        message = Message(other)
        return message + self

    @property
    def cqcode(self) -> str:
        data = (',' + ','.join([f'{k}={v}' for k, v in self.data.items()])) if self.data else ''
        return f'[CQ:{self.type}{data}]'

    @property
    def dict(self) -> dict[str, Any]:
        return dict(type=self.type, data=self.data)
    
    #region 协议消息段
    @staticmethod
    def text(text: str) -> MessageSegment:
        '''
        ## 纯文本
        
        ---
        ### 参数
        * text: 纯文本内容
        '''
        return MessageSegment('text', {'text': text})

    @staticmethod
    def face(id: str) -> MessageSegment:
        '''
        ## QQ 表情
        
        ---
        ### 参数
        * id: QQ 表情 ID
        '''
        return MessageSegment('face', {'id': id})
    
    @staticmethod
    def image(file: Union[str, Path, bytes, Image, BytesIO], **kwargs: Any) -> MessageSegment:
        '''
        ## 图片
        
        ---
        ### 参数
        * file: 图片文件
            - 绝对路径
            - 网络 URL
            - Base64 编码
            - Image 实例
            - Path
            - bytes
            - BytesIO
        '''
        if isinstance(file, BytesIO):
            file = file.getvalue()
        if isinstance(file, bytes):
            file = 'base64://'+b64encode(file).decode()
        elif isinstance(file, Path):
            file = file.resolve().as_uri()
        elif isinstance(file, Image):
            io = BytesIO()
            file.save(io, format='PNG')
            file = 'base64://'+b64encode(io.getvalue()).decode()
        return MessageSegment('image', {'file': file, **kwargs})


    @staticmethod
    def record(file: Union[str, Path, bytes, BytesIO], **kwargs: Any) -> MessageSegment:
        '''
        ## 语音
        
        ---
        ### 参数
        * file: 语音文件
            - 绝对路径
            - 网络 URL
            - Base64 编码
            - Path
            - bytes
            - BytesIO
        '''
        if isinstance(file, BytesIO):
            file = file.getvalue()
        if isinstance(file, bytes):
            file = 'base64://'+b64encode(file).decode()
        elif isinstance(file, Path):
            file = file.resolve().as_uri()
        return MessageSegment('record', {'file': file, **kwargs})
    
    @staticmethod
    def video(file: Union[str, Path, bytes, BytesIO], **kwargs: Any) -> MessageSegment:
        '''
        ## 视频
        
        ---
        ### 参数
        * file: 视频文件
            - 绝对路径
            - 网络 URL
            - Base64 编码
            - Path
            - bytes
            - BytesIO
        '''
        if isinstance(file, BytesIO):
            file = file.getvalue()
        if isinstance(file, bytes):
            file = 'base64://'+b64encode(file).decode()
        elif isinstance(file, Path):
            file = file.resolve().as_uri()
        return MessageSegment('video', {'file': file, **kwargs})

    @staticmethod
    def at(qq: str, **kwargs: Any) -> MessageSegment:
        '''
        ## 艾特某人
        
        ---
        ### 参数
        * qq: QQ 号
        '''
        return MessageSegment('at', {'qq': qq, **kwargs})

    @staticmethod
    def rps() -> MessageSegment:
        '''
        ## 猜拳
        '''
        return MessageSegment('rps', dict())

    @staticmethod
    def dice() -> MessageSegment:
        '''
        ## 骰子
        '''
        return MessageSegment('dice', dict())

    @staticmethod
    def music(type: str, id: str) -> MessageSegment:
        '''
        ## 音乐分享
        
        ---
        ### 参数
        * type: 音乐平台
            - qq
            - 163
            - xm
        * id: 歌曲 ID
        '''
        return MessageSegment('music', {'type': type, 'id': id})

    @staticmethod
    def reply(id: str) -> MessageSegment:
        '''
        ## 回复
        
        ---
        ### 参数
        * id: 消息 ID
        '''
        return MessageSegment('reply', {'id': id})

    @staticmethod
    def node(id: Optional[str] = None, nickname: str = 'Ritsu', content: Union[str, MessageSegment, Message] = '', **kwargs: Any) -> MessageSegment:
        '''
        ## 合并转发节点
        
        ---
        ### 参数
        * id: 消息 ID 若设置此项则无视`nickname`, `content`
        * nickname: 发送者昵称
        * content: 消息内容
        '''
        if id is not None:
            return MessageSegment('node', {'id': id})
        else:
            return MessageSegment('node', {'nickname': nickname, 'content': content, **kwargs})

    @staticmethod
    def json(data: str, **kwargs: Any) -> MessageSegment:
        '''
        ## JSON 消息
        
        ---
        * data: JSON 内容
        '''
        return MessageSegment('json', {'data': data, **kwargs})
    #endregion

_CQCODE_PATTERN = r'\[CQ:(?P<type>\w+),?(?P<data>(?:\w+=[^,\[\]]+,?)*)\]'

def _generate_segment(cqcode: str) -> Generator[MessageSegment, Any, None]:
    seq = 0
    for matched in re_finditer(_CQCODE_PATTERN, cqcode):
        if seq < (k := matched.start()):
            yield MessageSegment('text', {'text': cqcode[seq:k]})
        data = matched.group('data')
        yield MessageSegment(matched.group('type'), {k: v for k, v in [d.split('=', 1) for d in data.split(',') if d]})
        seq = matched.end()
    if seq+1 <= len(cqcode):
        yield MessageSegment('text', {'text': cqcode[seq:]})

class Message:
    '''# 消息'''
    
    __slots__ = ('segments', )
    
    segments: list[MessageSegment]

    def __init__(self, message: Optional[Union[MessageLike, MessageArray]] = None) -> None:
        self.segments = list()
        if message is None:
            pass
        elif isinstance(message, Message):
            self.segments.extend(message.segments)
        elif isinstance(message, MessageSegment):
            self.segments.append(message)
        elif isinstance(message, list):
            self.segments.extend([MessageSegment(**segment) for segment in message])
        elif isinstance(message, dict):
            self.segments.append(MessageSegment(**message))
        else:
            self.segments.extend(_generate_segment(message))
    
    def __iter__(self) -> Generator[MessageSegment, Any, None]:
        for segment in self.segments:
            yield segment
    
    @overload
    def __getitem__(self, v: int) -> MessageSegment:...

    @overload
    def __getitem__(self, v: slice) -> list[MessageSegment]:...

    def __getitem__(self, v: Union[int, slice]) -> Union[MessageSegment, list[MessageSegment]]:
        return self.segments[v]

    def __str__(self) -> str:
        return ''.join([str(segment) for segment in self.segments])

    def __repr__(self) -> str:
        return f'Message({self.segments})'

    def __add__(self, other: MessageLike) -> Self:
        if isinstance(other, Message):
            self.segments.extend(other.segments)
        elif isinstance(other, MessageSegment):
            self.segments.append(other)
        else:
            self.segments.extend(_generate_segment(other))
        return self

    def __radd__(self, other: MessageLike) -> Self:
        if isinstance(other, Message):
            self.segments.extend(other.segments)
        elif isinstance(other, MessageSegment):
            self.segments.append(other)
        else:
            self.segments.extend(_generate_segment(other))
        return self

    @property
    def array(self) -> list[dict[str, Any]]:
        return [segment.dict for segment in self]


MessageLike = Union[Message, MessageSegment, str]
MessageArray = Union[list[dict[str, Any]], dict[str, Any]]

class MessageJSONEncoder(JSONEncoder):
    
    def default(self, o: Any):
        if isinstance(o, Message):
            return o.array
        elif isinstance(o, MessageSegment):
            return Message(o).array
        return super().default(o)


__all__ = [
    'Message',
    'MessageSegment',
    'MessageLike',
    'MessageArray',
    'MessageJSONEncoder',
]