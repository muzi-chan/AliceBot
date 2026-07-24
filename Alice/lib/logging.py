from pathlib import Path
from sys import exc_info

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from multiprocessing import current_process
from time import time
from threading import current_thread
from typing import Any, Callable, Optional, TextIO, Union
from types import TracebackType


def rgb(obj: Any, r: int, g: int, b: int, fg: bool = True) -> str:
    m = '38' if fg else '48'
    return f'\033[{m};2;{r};{g};{b}m' + str(obj) + '\033[0m'

def rgb_wrap(r: int, g: int, b: int, fg: bool = True) -> Callable[..., str]:
    c = '\033[' + ('38' if fg else '48') + f';2;{r};{g};{b}m'
    del r, g, b, fg
    def wrap(obj: Any) -> str:
        return c + str(obj) + '\033[0m'
    return wrap

def style(obj: Any, *styles: str) -> str:
    if styles:
        return '\033[' + ';'.join(styles) + 'm' + str(obj) + '\033[0m'
    return str(obj)

def style_wrap(*styles: str) -> Callable[..., str]:
    s = '\033[' + ';'.join(styles) + 'm'
    def wrap(obj: Any) -> str:
        return s + str(obj) + '\033[0m'
    return wrap

# Log Level
FATAL = 100
ERROR = 80
WARNING = 60
SUCCESS = 40
INFO = 20
TRACE = 10
DEBUG = 0

_LEVELS = {
    'FATAL':     FATAL    ,
    'ERROR':     ERROR    ,
    'WARNING':   WARNING  ,
    'SUCCESS':   SUCCESS  ,
    'INFO':      INFO     ,
    'TRACE':     TRACE    ,
    'DEBUG':     DEBUG    ,
}

_STYLES = {
    'FATAL':     rgb_wrap(255,   0,   0),
    'ERROR':     rgb_wrap(231,  51,  24),
    'WARNING':   rgb_wrap(247, 163,   0),
    'SUCCESS':   rgb_wrap(  0, 204,   0),
    'INFO':      rgb_wrap( 51, 153, 255),
    'TRACE':     rgb_wrap(255, 182, 230),
    'DEBUG':     rgb_wrap(178, 178, 178),
}

def add_level(name: str, value: int, style_wrap: Callable[..., str]) -> None:
    ln = name.upper()
    assert ln not in _LEVELS, f'level {ln} already exists.'
    _LEVELS[ln] = value
    _STYLES[ln] = style_wrap

def del_level(name: str) -> None:
    ln = name.upper()
    assert ln in _LEVELS, f'level {ln} not exists.'
    _STYLES.pop(name)

def get_level_style(name: str) -> Callable[..., str]:
    return _STYLES.get(name.upper(), _STYLES['INFO'])

def change_level_style(name: str, style_wrap: Callable[..., str]) -> None:
    ln = name.upper()
    assert ln in _LEVELS, f'level {ln} not exists.'
    _STYLES[ln] = style_wrap

@dataclass(eq=False, repr=False, slots=True)
class RecordThread:
    id: int
    name: str


@dataclass(eq=False, repr=False, slots=True)
class RecordProcess:
    id: int
    name: str


@dataclass(eq=False, repr=False, slots=True)
class RecordException:
    type: Optional[type[BaseException]]
    value: Optional[BaseException]
    traceback: Optional[TracebackType]


@dataclass(eq=False, repr=False, slots=True)
class Record:
    time: datetime
    level: str
    msg: object
    exception: Optional[RecordException] = None
    extra: Any = None
    
    @property
    def thread(self) -> RecordThread:
        ct = current_thread()
        return RecordThread(ct.ident, ct.name) # type: ignore
    
    @property
    def process(self) -> RecordProcess:
        cp = current_process()
        return RecordProcess(cp.ident, cp.name) # type: ignore


_DEFAULT_FORMAT_TEMPLATE = '{year}-{month}-{day} {hour:02d}:{minute:02d}:{second:02d} [{level}] {msg}'

class Formatter:
    
    __slots__ = ('template', )

    def __init__(self, template: str = _DEFAULT_FORMAT_TEMPLATE) -> None:
        self.template = template
    
    def __call__(self, record: Record) -> str:
        T = record.time
        log = self.template.format(year=T.year, month=T.month, day=T.day, hour=T.hour, minute=T.minute, second=T.second, level=record.level, msg=str(record.msg))
        log = self.check_end(log)
        if (re := record.exception) is not None:
            log = self.check_end(log + self.exception(re))
        return log

    @staticmethod
    def exception(record_exception: RecordException) -> str:
        if record_exception.type is None:
            return ''
        et = '    Traceback (most recent call last):\n'
        tb = record_exception.traceback
        while tb:
            frame = tb.tb_frame
            et += f'        File \"{frame.f_code.co_filename}\", line {tb.tb_lineno}, in {frame.f_code.co_name}\n'
            tb = tb.tb_next
        et += f'    {record_exception.type.__name__}: {record_exception.value}.'
        return et
    
    @staticmethod
    def check_end(log: str) -> str:
        return log if log.endswith('\n') else f'{log}\n'


class Stream:
    
    __slots__ = ('io', 'level', 'formatter')
    
    io: TextIO
    level: int
    formatter: Callable[[Record], str]
    
    def __init__(self, io: TextIO, level: int = INFO) -> None:
        self.io = io
        self.level = level
        self.formatter = Formatter()

    def write(self, record: Record) -> None:
        if _LEVELS.get(record.level, INFO) < self.level:
            return
        
        log = self.formatter(record)
        self.io.write(log)
        self.io.flush()


class FileStream(Stream):

    __slots__ = ('io', 'level', 'formatter', 'dir', '__ndt')
    
    dir: Path
    __ndt: float
    
    def __init__(self, dir: Path, level: int = INFO) -> None:
        self.dir = dir
        self.level = level
        self.formatter = Formatter()
        self.dir.mkdir(parents=True, exist_ok=True)
        self.new_log_file(True)
    
    def new_log_file(self, init: bool = False) -> None:
        if not init and not self.io.closed:
            self.io.close()
        td = date.today()
        nd = td + timedelta(1)
        self.io = open(self.dir / f'{td}.log', 'a', encoding='UTF-8')
        self.__ndt = datetime(nd.year, nd.month, nd.day).timestamp()
    
    def write(self, record: Record) -> None:
        if time() > self.__ndt:
            self.new_log_file()
        super().write(record)


def _record_factory(level: str, msg: object, exc: bool, extra: Any = None) -> Record:
    T = datetime.now()
    re = RecordException(*exc_info()) if exc else None
    record = Record(T, level, msg, re, extra)
    return record

class Logger:
    
    __slots__ = ('_level', '_streams', '_record_factory')
    
    _level: int
    _streams: list[Stream]
    _record_factory: Callable[[str, object, bool, Any], Record]
    
    def __init__(self, level: int = INFO) -> None:
        self._level = level
        self._record_factory = _record_factory
        self._streams = list()
    
    def add_stream(self, stream: Stream) -> None:
        self._streams.append(stream)
    
    def set_level(self, level: Union[int, str]) -> None:
        if isinstance(level, int):
            self._level = level
        else:
            ln = level.upper()
            assert ln in _LEVELS
            self._level = _LEVELS[ln]
    
    def set_record_factory(self, record_factory: Callable[[str, object, bool, Any], Record]) -> None:
        self._record_factory = record_factory
    
    @property
    def level(self) -> int:
        return self._level
    
    @property
    def streams(self) -> list[Stream]:
        return self._streams
    
    def fork(self, level: Optional[Union[int, str]] = None) -> 'Logger':
        if level is None:
            level = INFO
        elif isinstance(level, str):
            ln = level.upper()
            assert ln in _LEVELS
            level = _LEVELS[ln]
        
        new_logger = Logger(level)
        for stream in new_logger.streams:
            new_logger.add_stream(stream)

        return new_logger
    
    def log(self, level: str, msg: object, exc: bool = False, extra: Any = None) -> None:
        lvl = _LEVELS.get(level, INFO)
        if lvl < self._level:
            return
        record = self._record_factory(level, msg, exc, extra)
        for stream in self._streams:
            if lvl < stream.level:
                continue
            stream.write(record)
    
    def fatal(self, msg: object, exc: bool = True, extra: Any = None) -> None:
        self.log('FATAL', msg, exc, extra)

    def error(self, msg: object, exc: bool = True, extra: Any = None) -> None:
        self.log('ERROR', msg, exc, extra)

    def warning(self, msg: object, exc: bool = False, extra: Any = None) -> None:
        self.log('WARNING', msg, exc, extra)

    def success(self, msg: object, exc: bool = False, extra: Any = None) -> None:
        self.log('SUCCESS', msg, exc, extra)

    def info(self, msg: object, exc: bool = False, extra: Any = None) -> None:
        self.log('INFO', msg, exc, extra)

    def trace(self, msg: object, exc: bool = False, extra: Any = None) -> None:
        self.log('TRACE', msg, exc, extra)

    def debug(self, msg: object, exc: bool = False, extra: Any = None) -> None:
        self.log('DEBUG', msg, exc, extra)


__all__ = [
    'FATAL',
    'ERROR',
    'WARNING',
    'SUCCESS',
    'INFO',
    'TRACE',
    'DEBUG',
    'rgb',
    'rgb_wrap',
    'style',
    'style_wrap',
    'add_level',
    'del_level',
    'get_level_style',
    'change_level_style',
    'Record',
    'Formatter',
    'Stream',
    'FileStream',
    'Logger',
]