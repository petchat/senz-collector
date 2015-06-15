__author__ = 'jiaying.lu'

__all__ = ["LOGENTRIES_TOKEN", "ROLLBAR_TOKEN", "APP_ENV"]
import os

# Settings

LOGENTRIES_DEV_TOKEN = "6780de1b-f4c2-47ad-9698-146d583833d6"
LOGENTRIES_PROD_TOKEN = "184e19de-3291-447b-baa2-e36b50f75592"
LOGENTRIES_LOCAL_TOKEN = "6780de1b-f4c2-47ad-9698-146d583833d6"

ROLLBAR_DEV_TOKEN = "4b6aba13553f44ba87bef96c176c6208"
ROLLBAR_PROD_TOKEN = "6b773c84e86041798a513ba8ef73bb74"
ROLLBAR_LOCAL_TOKEN = "4b6aba13553f44ba87bef96c176c6208"

LOGENTRIES_TOKEN = ""
ROLLBAR_TOKEN = ""
APP_ENV = ""

# Configuration

try:
    APP_ENV = os.environ["APP_ENV"]
except KeyError, key:
    print "KeyError: There is no env var named %s" % key
    print "The local env will be applied"
    APP_ENV = "local"
finally:
    if APP_ENV == "dev":
        LOGENTRIES_TOKEN = LOGENTRIES_DEV_TOKEN
        ROLLBAR_TOKEN = ROLLBAR_DEV_TOKEN
    elif APP_ENV == "prod":
        LOGENTRIES_TOKEN = LOGENTRIES_PROD_TOKEN
        ROLLBAR_TOKEN = ROLLBAR_PROD_TOKEN
    elif APP_ENV == "local":
        LOGENTRIES_TOKEN = LOGENTRIES_LOCAL_TOKEN
        ROLLBAR_TOKEN = ROLLBAR_LOCAL_TOKEN