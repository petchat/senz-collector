__author__ = 'jiaying.lu'

__all__ = ["LOGENTRIES_TOKEN", "BUGSNAG_TOKEN", "APP_ENV"]
import os

# Settings

LOGENTRIES_DEV_TOKEN = "6780de1b-f4c2-47ad-9698-146d583833d6"
LOGENTRIES_PROD_TOKEN = "184e19de-3291-447b-baa2-e36b50f75592"
LOGENTRIES_LOCAL_TOKEN = "6780de1b-f4c2-47ad-9698-146d583833d6"

BUGSNAG_DEV_TOKEN = "7fc0227c206a95c13129c7e2e2d192bf"
BUGSNAG_PROD_TOKEN = "0d81e1ddd34840e28ae6a4c17dd1fa81"
BUGSNAG_LOCAL_TOKEN = "7fc0227c206a95c13129c7e2e2d192bf"

LOGENTRIES_TOKEN = ""
BUGSNAG_TOKEN = ""
APP_ENV = ""

# Configuration

try:
    APP_ENV = os.environ["APP_ENV"]
except KeyError, key:
    print "KeyError: There is no env var named %s" % key
    print "The local env will be applied"
    APP_ENV = "local"
finally:
    if APP_ENV == "test":
        LOGENTRIES_TOKEN = LOGENTRIES_DEV_TOKEN
        BUGSNAG_TOKEN = BUGSNAG_DEV_TOKEN
    elif APP_ENV == "prod":
        LOGENTRIES_TOKEN = LOGENTRIES_PROD_TOKEN
        BUGSNAG_TOKEN = BUGSNAG_PROD_TOKEN
    elif APP_ENV == "local":
        LOGENTRIES_TOKEN = LOGENTRIES_LOCAL_TOKEN
        BUGSNAG_TOKEN = BUGSNAG_LOCAL_TOKEN