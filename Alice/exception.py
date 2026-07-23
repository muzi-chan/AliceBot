class AliceException(Exception):
    '''# Alice统一异常类'''


class ActionDone(AliceException):
    '''# 行动完成'''


class APICallingFailed(AliceException):
    '''# 调用API失败'''


class APICallingTimeout(APICallingFailed):
    '''# 调用API超时'''


class APINotImplemented(APICallingFailed):
    '''# 调用API未实现'''


class APIBotNotConnected(APICallingFailed):
    '''# 调用API时所属机器人未连接'''


class ExistAliceCore(AliceException):
    '''# 已存在Alice核心实例'''


class PluginCircularDependency(AliceException):
    '''# 插件循环依赖'''


class RequireExplicitParam(AliceException):
    '''# 需要显式输入的参数'''
    


__all__ = [
    'AliceException',
    'ExistAliceCore',
    'ActionDone',
]