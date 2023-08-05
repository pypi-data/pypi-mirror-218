"""
module contain the utility functions
"""
import inspect
from datetime import datetime
from . import environments


def get_calling_module_name(stack) -> str:
    """
    method responsible for returning the log calling file
    :param stack: calling module stack
    :return: file name
    """
    # get module handle from stack object
    module = inspect.getmodule(stack[1][0])
    # get module path
    module_whole_path = module.__file__
    # get the file name
    file_name = module_whole_path.split("\\")[-1]
    return file_name


def get_current_date_time_str() -> str:
    """
    responsible for returning the current date time str in requested format
    :return: current datetime str
    """
    # get current date time
    current_time = datetime.now()
    # convert current datetime value into desired datetime format str
    return current_time.strftime(environments.log_date_time_format)


def display_log(log_mode: str, calling_module: str, date_time: str, message:str) -> None:
    """
    function to print date for logging
    :param log_mode: DEBUG, INFO, WARNING, ERROR, CRITICAL
    :param calling_module: main.py, application.py
    :param date_time: 2023-07-06 14:19:10
    :param message: warning message
    :return: None
    """
    print(f"[{log_mode}]::[{calling_module}]::[{date_time}]:: [{message}]")
