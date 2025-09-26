"""
GameLogger - Logging spécialisé pour développement
"""

import logging
import sys
from datetime import datetime

class GameLogger:
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger("StripSexSeduce")
        self.logger.setLevel(level)

        # Handler console
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)
