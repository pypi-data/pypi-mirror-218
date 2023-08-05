"""
module of customer logger class
"""
import inspect
from . import environments
from .log_utils import get_calling_module_name, get_current_date_time_str, display_log
from .logger_mode import LogMode


class CustomLogger:
    """
    custom logger declaration
    """
    @staticmethod
    def debug(message: str) -> None:
        """
        for display the debug log message
        :param message: "debug message"
        :return: None
        """
        if LogMode.DEBUG.value >= environments.log_mode:
            display_log(LogMode.DEBUG.name,
                        get_calling_module_name(inspect.stack()),
                        get_current_date_time_str(),
                        message)

    @staticmethod
    def info(message: str) -> None:
        """
        for display the info log message
        :param message: "info message"
        :return: None
        """
        if LogMode.INFO.value >= environments.log_mode:
            display_log(LogMode.INFO.name,
                        get_calling_module_name(inspect.stack()),
                        get_current_date_time_str(),
                        message)

    @staticmethod
    def warning(message: str) -> None:
        """
        for display the warning log message
        :param message: "warning message"
        :return: None
        """
        if LogMode.WARNING.value >= environments.log_mode:
            display_log(LogMode.WARNING.name,
                        get_calling_module_name(inspect.stack()),
                        get_current_date_time_str(),
                        message)

    @staticmethod
    def error(message: str) -> None:
        """
        for display the error log message
        :param message: "error message"
        :return: None
        """
        if LogMode.ERROR.value >= environments.log_mode:
            display_log(LogMode.ERROR.name,
                        get_calling_module_name(inspect.stack()),
                        get_current_date_time_str(),
                        message)

    @staticmethod
    def critical(message: str) -> None:
        """
        for display the critical log message
        :param message: "critical message"
        :return: None
        """
        if LogMode.CRITICAL.value >= environments.log_mode:
            display_log(LogMode.CRITICAL.name,
                        get_calling_module_name(inspect.stack()),
                        get_current_date_time_str(),
                        message)
