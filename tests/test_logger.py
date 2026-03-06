import logging
import os
import pytest
import re

from pathlib import Path

from app.logger import CustomLogger

def test_logging_setup():

    # Check log paths and that data was written to the log file

    log_file = Path('./test_logging_setup/test.log')
    if os.path.exists(log_file):
        os.remove(log_file)
    CustomLogger.setup_logging(log_file)
    logging.info('Hello world!')

    with open(log_file, 'r') as in_f:
        actual = in_f.read()

    assert re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} - INFO - Logging initialized at: .*/test_logging_setup/test\.log.*Hello world!$',
                    actual,
                    flags=re.DOTALL
    ) is not None

def test_fail_setup_logging():

    # Simulate error in setting up logging

    with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'parent'"):
        CustomLogger.setup_logging(None)
