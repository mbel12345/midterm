import logging
import os

from pathlib import Path

class Logger:

    @staticmethod
    def setup_logging(log_file: Path) -> None:

        # Configure Calculator logging

        try:

            # Make sure log dir exists
            os.makedirs(log_file.parent, exist_ok=True)
            log_file = log_file.resolve()

            # Configure logging settings
            logging.basicConfig(
                filename=str(log_file),
                level = logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                force=True,
            )
            Logger.info(f'Logging initialized at: {log_file}')

        except Exception as e:

            print(f'Error setting up logging: {e}')
            raise

    @staticmethod
    def info(message):

        logging.info(message)

    @staticmethod
    def warning(message):

        logging.warning(message)

    @staticmethod
    def error(message):

        logging.error(message)
