import logging
import os
import pytest
import re

from pathlib import Path

from app.logger import Logger

timestamp_regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}'

def test_logging_setup():

    # Check log paths and that data was written to the log file

    log_file = Path('./test_logger/test_logging_setup.log')
    if os.path.exists(log_file):
        os.remove(log_file)
    Logger.setup_logging(log_file)
    logging.info('Hello world!')

    with open(log_file, 'r') as in_f:
        actual = in_f.read()

    assert re.match(f'^{timestamp_regex} - INFO - Logging initialized at: .*/test_logger/test_logging_setup.log.*Hello world!$',
                    actual,
                    flags=re.DOTALL
    ) is not None

def test_fail_setup_logging():

    # Simulate error in setting up logging

    with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'parent'"):
        Logger.setup_logging(None)

def test_logger_info():

    # Test Logger.info()

    log_file = Path('./test_logger/test_logger_info.log')
    if os.path.exists(log_file):
        os.remove(log_file)
    Logger.setup_logging(log_file)
    Logger.info('Hello world!')

    with open(log_file, 'r') as in_f:
        actual = in_f.read()

    assert re.search(f'{timestamp_regex} - INFO - Hello world!.*',
                    actual,
                    flags=re.DOTALL
    ) is not None

def test_logger_warning():

    # Test Logger.warning()

    log_file = Path('./test_logger/test_logger_warning.log')
    if os.path.exists(log_file):
        os.remove(log_file)
    Logger.setup_logging(log_file)
    Logger.warning('Hello world!')

    with open(log_file, 'r') as in_f:
        actual = in_f.read()

    assert re.search(f'{timestamp_regex} - WARNING - Hello world!.*',
                    actual,
                    flags=re.DOTALL
    ) is not None

def test_logger_error():

    # Test Logger.warning()

    log_file = Path('./test_logger/test_logger_error.log')
    if os.path.exists(log_file):
        os.remove(log_file)
    Logger.setup_logging(log_file)
    Logger.error('Hello world!')

    with open(log_file, 'r') as in_f:
        actual = in_f.read()

    assert re.search(f'{timestamp_regex} - ERROR - Hello world!.*',
                    actual,
                    flags=re.DOTALL
    ) is not None
