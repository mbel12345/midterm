import logging
import os

from pathlib import Path

class CustomLogger:

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
            logging.info(f'Logging initialized at: {log_file}')

        except Exception as e:

            print(f'Error setting up logging: {e}')
            raise
