"""Provide log for other modules"""

from logentries import LogentriesHandler
import logging

__all__ = ['logger']

logger = logging.getLogger('logentries')
logger.setLevel(logging.INFO)
LOGENTRIES_TOKEN = '184e19de-3291-447b-baa2-e36b50f75592'
logentries_handler = LogentriesHandler(LOGENTRIES_TOKEN)

logger.addHandler(logentries_handler)
