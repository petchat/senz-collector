"""Provide log for other modules"""

from config import LOGENTRIES_TOKEN
from logentries import LogentriesHandler
import logging

__all__ = ['logger']

logger = logging.getLogger('rollbar')
logger.setLevel(logging.INFO)
logentries_handler = LogentriesHandler(LOGENTRIES_TOKEN)

logger.addHandler(logentries_handler)
