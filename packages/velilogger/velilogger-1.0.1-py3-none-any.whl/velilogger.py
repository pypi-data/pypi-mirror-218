import contextvars
import logging
import os
import uuid

tracing_id = contextvars.ContextVar("tracing_id", default=None)
APP_NAME = os.environ.get("APP_NAME", 'not_specified')


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.tracing_id = get_tracing_id()
        return True


def generate_tracing_id(value=None):
    if value:
        tracing_id.set(value)
        return value
    if not tracing_id.get():
        _id = uuid.uuid4().__str__()
        tracing_id.set(_id)
        return _id
    return tracing_id.get()


def get_tracing_id():
    return tracing_id.get()


logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)

veli_log_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(tracing_id)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(veli_log_formatter)
stream_handler.addFilter(ContextFilter())

logger.addHandler(stream_handler)
