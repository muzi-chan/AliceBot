import re


_VERSION_PATTERN = r'^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:-(?P<prerelease>[a-zA-Z0-9.-]+))?(?:\+(?P<build>[a-zA-Z0-9.-]+))?$'

class Version:
    '''
    # 版本
    
    ---
    支持格式: `major.minor.patch[+build][-prerelease]`
    '''
    __slots__ = ('major', 'minor', 'patch', 'prerelease', 'build', 'original')
    
    major: int
    minor: int
    patch: int
    prerelease: tuple[str, ...]
    build: tuple[str, ...]
    original: str
    
    def __init__(self, version: str) -> None:
        '''
        ## 初始化版本
        
        ---
        version: 版本字符串, 支持格式: `major.minor.patch[+build][-prerelease]`
        '''
        match = re.match(_VERSION_PATTERN, version)
        assert match is not None, '不支持的版本格式'
        group = match.groupdict()
        self.major = int(group['major'])
        self.minor = int(group['minor'])
        self.patch = int(group['patch'])
        self.prerelease = tuple() if group['prerelease'] is None else tuple(group['prerelease'].split('.'))
        self.build = tuple() if group['build'] is None else tuple(group['build'].split('.'))
        self.original: str = version

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.prerelease == other.prerelease
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch
        
        if not other.prerelease and self.prerelease:
            return True
        
        return self.prerelease < other.prerelease

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return not (self <= other)

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return not (self < other)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return not (self == other)

    def __repr__(self) -> str:
        return f'Version({self.original!r})'

    def __str__(self) -> str:
        return self.original


__all__ = [
    'Version',
]