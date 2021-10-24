from loguru import logger
import inspect
import sys


class BaseLogger:
    count = 0

    def __init__(self):
        self.count += 1
        logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: "
                                                     "<8}</level> | <level>{message}</level>")
        print(f"Init BaseLogger: {self.count}")

    def debug(self, msg, data={}):
        prefix = self.get_pre_fix()
        logger.debug(f"{prefix} | {msg}")

    def info(self, msg, data={}):
        prefix = self.get_pre_fix()
        logger.info(f"{prefix} | {msg}")

    def warning(self, msg, data={}):
        prefix = self.get_pre_fix()
        logger.warning(f"{prefix} | {msg}")

    def error(self, msg, data={}):
        prefix = self.get_pre_fix()
        logger.error(f"{prefix} | {msg}")

    def exception(self, msg, data={}):
        prefix = self.get_pre_fix()
        logger.exception(f"{prefix} | {msg}")

    def get_pre_fix(self):
        last_stack_call = inspect.stack()[2]
        func = last_stack_call.function
        filename = last_stack_call.filename
        lineno = last_stack_call.lineno
        return f"{filename} | {func}:{lineno}"


base_logger = BaseLogger()
