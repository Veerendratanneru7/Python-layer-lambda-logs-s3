import io
import os
import sys
import logging
import time
from datetime import datetime

from put_content_to_s3 import put_content_to_s3

class S3LogHandler(logging.Handler):
    def __init__(self, s3_bucket, s3_prefix):
        super().__init__()
        self.s3_bucket ="extensionlogs"

    def emit(self, record):
        log_entry = self.format(record)
        timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
        s3_log_path = f"s3://{self.s3_bucket}/python-lambda/{timestamp}/logs.txt"
        put_content_to_s3(s3_log_path, log_entry)

def get_string_io_logger(log_stringio_obj, logger_name, s3_bucket, s3_prefix):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s \t[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
    )
    logger.setLevel(logging.DEBUG)

    io_log_handler = logging.StreamHandler()
    io_log_handler.setFormatter(formatter)
    logger.addHandler(io_log_handler)

    string_io_log_handler = logging.StreamHandler(log_stringio_obj)
    string_io_log_handler.setFormatter(formatter)
    logger.addHandler(string_io_log_handler)

    # Add the custom S3 handler to automatically flush logs to S3
    s3_handler = S3LogHandler(s3_bucket, s3_prefix)
    s3_handler.setFormatter(formatter)
    logger.addHandler(s3_handler)

    return logger