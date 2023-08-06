import datetime

from .ConsoleColors import ConsoleColors
from .logPLevel import logPLevel
from .util import *

# 等级
level = logPLevel.INFO


# 日志输出
def _base(args, sep=' ', end='\n', file=None, _level=logPLevel.INFO, color=ConsoleColors.RESET):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    args = "{:<20} {:<8} {}  {}".format(timestamp, get_caller_file_basename_path(), _level['name'], args)
    args = f"{color}{args}{ConsoleColors.RESET}"
    if _level['level'] >= level['level']:
        print(args, sep=sep, end=end, file=file)


# info等级
def info(args, sep=' ', end='\n', file=None):
    _base(args, sep, end, file, logPLevel.INFO, ConsoleColors.RESET)


# warning等级
def warning(args, sep=' ', end='\n', file=None):
    _base(args, sep, end, file, logPLevel.WARNING, ConsoleColors.YELLOW)


# error等级
def error(args, sep=' ', end='\n', file=None):
    _base(args, sep, end, file, logPLevel.ERROR, ConsoleColors.RED)


# debug等级
def debug(args, sep=' ', end='\n', file=None):
    _base(args, sep, end, file, logPLevel.DEBUG, ConsoleColors.RED)


# critical等级
def critical(args, sep=' ', end='\n', file=None):
    _base(args, sep, end, file, logPLevel.CRITICAL, ConsoleColors.RED)
