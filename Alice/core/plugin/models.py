from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from Alice.lib.version import Version


class PluginAuthor(BaseModel):
    '''# 插件作者'''
    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)

    name: str
    '''## 名称'''
    link: Optional[list[str]] = None
    '''## 连接'''
    avatar: Optional[Path] = None
    '''## 头像'''
    description: Optional[str] = None
    '''## 简介'''


class PluginDependency(BaseModel):
    '''# 插件依赖项'''
    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)
    
    id: str
    '''## 唯一插件标识符'''
    name: str
    '''## 插件显示名称'''
    optional: bool = False
    '''## 是否为可选的'''
    min_version: Optional[Version] = None
    '''## 最低所需版本'''
    max_version: Optional[Version] = None
    '''## 最高允许版本'''

    @field_validator('min_version', 'max_version', mode='before')
    @classmethod
    def _(cls, version: str) -> Version:
        return Version(version)


class PluginMetadata(BaseModel):
    '''# 插件元数据'''
    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)

    id: str
    '''## 唯一插件标识符'''
    name: str
    '''## 插件显示名称'''
    version: Version
    '''## 插件版本'''
    description: Optional[str] = None
    '''## 插件描述'''
    authors: Optional[list[PluginAuthor]] = None
    '''## 插件作者'''
    dependencies: Optional[list[PluginDependency]] = None
    '''## 依赖项'''
    
    @field_validator('version', mode='before')
    @classmethod
    def _(cls, version: str) -> Version:
        return Version(version)


class PluginConfig(BaseModel):
    '''# 插件配置'''
    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)


class PluginStatus(BaseModel):
    '''# 插件状态'''
    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)

    loaded: bool = False
    '''## 插件已导入'''


class PluginExport(BaseModel):
    '''
    # 插件导出项
    
    ---
    导出项存于AE虚拟包内, 使用导入语法导入即可
    ```
    import AE.name
    
    from AE.name import xxx
    ```
    推荐在 `AE` 目录下添加同名存根文件 `name.pyi`
    '''
    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)
    
    name: str
    items: dict[str, Any]

    
__all__ = [
    'PluginAuthor',
    'PluginDependency',
    'PluginMetadata',
    'PluginConfig',
    'PluginStatus',
    'PluginExport',
]