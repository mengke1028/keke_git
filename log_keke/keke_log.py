import logging
from colorlog import ColoredFormatter


class LogManager:
    def __init__(self, name='root', log_file_path=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 控制台处理器
        stream_handler = logging.StreamHandler()
        stream_formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )
        stream_handler.setFormatter(stream_formatter)
        self.logger.addHandler(stream_handler)

        # 文件处理器（如果指定了日志文件路径）
        if log_file_path:
            file_handler = logging.FileHandler(log_file_path)
            file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)

    def addLog(self, data, level=logging.DEBUG):
        """
        添加日志条目。
        :param data: 日志内容
        :param level: 日志级别，默认为DEBUG
        """
        if level == logging.DEBUG:
            self.logger.debug(data)
        elif level == logging.INFO:
            self.logger.info(data)
        elif level == logging.WARNING:
            self.logger.warning(data)
        elif level == logging.ERROR:
            self.logger.error(data)
        elif level == logging.CRITICAL:
            self.logger.critical(data)

    def switch_log_path(self, new_path):
        """
        切换日志文件存储路径。
        :param new_path: 新的日志文件路径
        """
        # 首先移除之前的文件处理器（如果有）
        for handler in self.logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                self.logger.removeHandler(handler)

        # 添加新的文件处理器
        file_handler = logging.FileHandler(new_path, encoding='utf-8')
        file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)

    def change_logger_name(self, new_name):
        """
        修改日志记录器的名称。
        :param new_name: 新的日志记录器名称
        """
        self.logger.name = new_name


# 使用示例
if __name__ == "__main__":
    log_manager = LogManager('MyApp', '/path/to/default/log/file.log')
    log_manager.addLog('This is a debug message.')

    # 切换日志存储路径
    new_path = '/new/path/to/log/file.log'
    log_manager.switch_log_path(new_path)
    log_manager.addLog('Logging after path switch.', logging.INFO)
