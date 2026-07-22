import sys
try:
    if sys.platform == 'win32':
        from winloop import run
    else:
        from uvloop import run
except:
    from asyncio import run


__all__ = [
    'run',
]