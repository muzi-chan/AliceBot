from pathlib import Path

from pydantic import BaseModel, ConfigDict


class AliceBaseConfig(BaseModel):
    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)


class AliceWebUIConfig(AliceBaseConfig):
    '''# WebUI服务配置'''
    enable: bool
    host: str
    port: int
    index: Path
    static: Path


class AliceWebSocketConfig(AliceBaseConfig):
    '''# WebSocket服务配置'''
    enable: bool
    name: str
    host: str
    port: int
    path: str


class AliceNetWorkConfig(AliceBaseConfig):
    '''# 网络配置'''
    web_ui: AliceWebUIConfig
    websocket_servers: list[AliceWebSocketConfig]


class AlicePluginConfig(AliceBaseConfig):
    '''# 插件配置'''
    workers: int
    '''## 工作者数'''
    max_active_ticks: int
    '''## 最大活动帧数'''


class AliceBotConfig(AliceBaseConfig):
    '''# 插件配置'''
    update_interval: int
    '''## 更新时间间隔'''


class AliceCoreConfig(AliceBaseConfig):
    '''# Alice全局配置'''
    network: AliceNetWorkConfig
    '''## 网络配置'''
    plugin: AlicePluginConfig
    '''## 插件配置'''
    bot: AliceBotConfig


RAW_DEFAULT_CONFIG = \
'''
network:
  web_ui:
    enable: true
    host: 127.0.0.1
    port: 18000
    index: index.html
    static: assets

  websocket_servers:
  - enable: true
    name: default
    host: 127.0.0.1
    port: 18001
    path: /alice


plugin:
  workers: 2
  max_active_ticks: 32


bot:
  update_interval: 600
'''

__all__ = [
    'AliceWebUIConfig',
    'AliceWebSocketConfig',
    'AliceNetWorkConfig',
    'AliceNetWorkConfig',
    'AlicePluginConfig',
    'AliceBotConfig',
    'AliceCoreConfig',
    'RAW_DEFAULT_CONFIG',
]