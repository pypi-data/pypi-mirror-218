import inspect
import os.path


def get_caller_file_path():
    stack = inspect.stack()
    stack_len = len(stack)
    if stack_len > 1:
        # 获取调用当前函数的调用者的文件路径
        caller_frame = stack[stack_len - 1]
        caller_file_path = caller_frame.filename
        return caller_file_path
    return 'unknown'


def get_caller_file_basename_path():
    return os.path.basename(get_caller_file_path())
