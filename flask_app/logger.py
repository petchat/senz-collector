"""Provide log for other modules"""

from logentries import LogentriesHandler
import logging

__all__ = ['logger']

logger = logging.getLogger('rollbar')
logger.setLevel(logging.INFO)
LOGENTRIES_TOKEN = '6780de1b-f4c2-47ad-9698-146d583833d6'
logentries_handler = LogentriesHandler(LOGENTRIES_TOKEN)

logger.addHandler(logentries_handler)
