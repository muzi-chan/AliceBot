from asyncio import Future, TimeoutError, wait_for
from time import monotonic
from typing import Any, Callable, Generic, Optional, ParamSpec, TypeVar, TYPE_CHECKING, get_args, get_origin

from pydantic import BaseModel, ConfigDict

from Alice.exception import APICallingFailed, APICallingTimeout, APIBotNotConnected

if TYPE_CHECKING:
    from Alice.core.bot.bot import AliceBot


def _return_none(_: Any) -> None:
    return

class AliceBotAPIModel(BaseModel):
    '''# AliceBot API返回模型'''
    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)


R = TypeVar('R')

class AliceBotAPIResponse(BaseModel, Generic[R]):
    '''# AliceBot API响应'''
    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)
    
    cost_time: float
    '''## API 调用耗时'''
    content: R
    '''## API 响应内容'''


P = ParamSpec('P')

class AliceBotAPI(Generic[P, R]):
    '''
    # AliceBot API装饰器
    
    声明API参数和返回模型
    
    ---
    ### 创建格式
    ```
    @AliceBotAPI
    def other_api(*, a: int, b: str, c: bool = False, d: float = ...) -> AliceBotAPIModel:
        """说明"""
        ... # 此处省略号用于条件检查
    ```
    对于函数参数内的省略号, 如果调用时未给出, 则不会包含在上报数据中
    '''
    
    name: str
    return_factory: Callable[[Any], R]
    default_params: dict[str, Any]
    
    def __init__(self, func: Callable[P, R]) -> None:
        self.name = func.__name__
        return_type: Optional[type[R]] = func.__annotations__.get('return', None)
        if return_type is None:
            self.return_factory = _return_none # type: ignore
        elif origin_type := get_origin(return_type):
            if origin_type is list and issubclass(model_type := get_args(return_type)[0], AliceBotAPIModel):
                self.return_factory = lambda datas: [model_type.model_validate(data) for data in datas] # type: ignore
            else:
                self.return_factory = origin_type # type: ignore
        elif issubclass(return_type, AliceBotAPIModel):
            self.return_factory = return_type.model_validate
        else:
            self.return_factory = return_type
        self.default_params = dict(filter(lambda t: t[1] != Ellipsis, (func.__kwdefaults__ or dict()).items()))
    
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> AliceBotAPICall[P, R]:
        params = self.default_params.copy()
        params.update(kwargs)
        return AliceBotAPICall(self, params)


class AliceBotAPICall(Generic[P, R]):
    '''# AliceBot API调用对象'''
    __slots__ = ('api', 'bot', 'fut', 'echo', 'params')
    
    api: AliceBotAPI[P, R]
    bot: AliceBot
    fut: Future[dict[str, Any]]
    echo: int
    params: dict[str, Any]

    def __init__(self, api: AliceBotAPI[P, R], params: dict[str, Any]) -> None:
        self.api = api
        self.echo = id(self)
        self.params = params

    async def __call__(self, bot: AliceBot, timeout: float = 10) -> AliceBotAPIResponse[R]:
        if bot.server is None:
            raise APIBotNotConnected
        self.bot = bot
        server = bot.server
        start = monotonic()
        self.fut = Future()
        server.put_call(self) # type: ignore
        try:
            result = await wait_for(self.fut, timeout)
        except TimeoutError:
            raise APICallingTimeout()
        except APIBotNotConnected as e:
            raise APIBotNotConnected from e
        finally:
            server._calls.pop(self.echo, None) # type: ignore
        if result['status'] == 'failed':
            raise APICallingFailed(self.api.name, result['retcode'], result['wording'])
        content = self.api.return_factory(result.get('data', None))
        return AliceBotAPIResponse(cost_time=monotonic() - start, content=content)


__all__ = [
    'AliceBotAPI',
    'AliceBotAPICall',
    'AliceBotAPIModel',
]