import logging


class FormatterExtra(logging.Formatter):
    # From: https://docs.python.org/3/library/logging.html#logrecord-attributes
    reserved = [
        'args',
        'asctime',
        'created',
        'exc_info',
        'filename',
        'funcName',
        'levelname',
        'levelno',
        'lineno',
        'message',
        'module',
        'msecs',
        'msg',
        'name',
        'pathname',
        'process',
        'processName',
        'relativeCreated',
        'stack_info',
        'thread',
        'threadName',
        # Custom
        'exc_text',
        'color_message',
    ]

    def format(self, record):
        extra = record.__dict__.copy()
        for key in self.reserved:
            extra.pop(key, None)
        if extra:
            record.msg += f' {extra}'
        return super().format(record)
