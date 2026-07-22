from sys import stderr as _stderr

from Alice.lib.logging import *


class _AliceFormatter(Formatter):
    
    def __call__(self, record: Record) -> str:
        T = record.time
        level = get_level_style(record.level)('▌')
        log = self.template.format(year=T.year, month=T.month, day=T.day, hour=T.hour, minute=T.minute, second=T.second, thread=record.thread.name, level=level, msg=str(record.msg))
        log = self.check_end(log)
        if (re := record.exception) is not None:
            log = self.check_end(log + self.exception(re))
        return log


_template = rgb('{year}-{month}-{day} ', 127, 184, 14) + rgb('{hour:02d}:{minute:02d}:{second:02d} ', 239, 91, 156) + rgb('[{thread}]', 51, 163, 220) + '{level} {msg}'
_formatter = _AliceFormatter(_template)
_stream = Stream(_stderr)
_stream.formatter = _formatter
logger = Logger()
logger.add_stream(_stream)


__all__ = [
    'logger',
]