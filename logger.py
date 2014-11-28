"""
    test_logger.py
    1. logger with rotating logs
    2. write is persistant immediately
"""

import logging
import logging.handlers
import config
import sys


"""
    name, name of app being logged
"""
def logger(name = None):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
    handler = logging.handlers.RotatingFileHandler(config.LOG_DIR + '/' + config.LOG,
                                                   maxBytes=config.LOG_MAX_BYTES,
                                                   backupCount=config.LOG_FILE_COUNT)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

