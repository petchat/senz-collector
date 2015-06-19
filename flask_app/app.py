# -*- coding: UTF-8 -*-
__author__ = 'woodie'

from flask import Flask, request
# from senz_collector import SenzCollector
import json
import os

from timesequence_align import collect_senz_lists
from config import *

import bugsnag
from bugsnag.flask import handle_exceptions

from logentries import LogentriesHandler
import logging

# Configure Logentries
logger = logging.getLogger('logentries')
logger.setLevel(logging.DEBUG)
logentries_handler = LogentriesHandler(LOGENTRIES_TOKEN)
logger.addHandler(logentries_handler)

# Configure Bugsnag
bugsnag.configure(
    api_key=BUGSNAG_TOKEN,
    project_root=os.path.dirname(os.path.realpath(__file__)),
)

app = Flask(__name__)

# Attach Bugsnag to Flask's exception handler
handle_exceptions(app)


@app.before_first_request
def init_before_first_request():
    import datetime

    init_tag = "[Initiation of Service Process]\n"
    logger.info('[init] enter init before_first_request')

    log_init_time = "Initiation START at: \t%s\n" % datetime.datetime.now()
    log_app_env = "Environment Variable: \t%s\n" % APP_ENV
    log_bugsnag_token = "Bugsnag Service TOKEN: \t%s\n" % BUGSNAG_TOKEN
    log_logentries_token = "Logentries Service TOKEN: \t%s\n" % LOGENTRIES_TOKEN
    logger.info(init_tag + log_init_time)
    logger.info(init_tag + log_app_env)
    logger.info(init_tag + log_bugsnag_token)
    logger.info(init_tag + log_logentries_token)


@app.route('/', methods=['POST'])
def senzCollectorAPI():
    logger = logging.getLogger('logentries.X-Request-Id')
    if request.headers.has_key('X-Request-Id') and request.headers['X-Request-Id']:
        print('has key and')
        logger.setLevel(logging.DEBUG)
        logentries_handler = LogentriesHandler(LOGENTRIES_TOKEN)
        formatter = logging.Formatter('%(asctime)s : %(levelname)s, ' + request.headers['X-Request-Id'] + ', %(message)s')
        logentries_handler.setFormatter(formatter)
        logger.addHandler(logentries_handler)

    logger.info('[senzCollector API] enter API')
    result = {'code': 1, 'message': ''}

    # params JSON validate
    try:
        incoming_data = json.loads(request.data)
    except ValueError, err_msg:
        logger.exception('[ValueError] err_msg: %s, params=%s' % (err_msg, request.data))
        result['message'] = 'Unvalid params: NOT a JSON Object'
        return json.dumps(result)

    # params key checking
    for key in ['filter', 'timelines']:
        if key not in incoming_data:
            logger.exception("[KeyError] params=%s, should have key: %s" % (incoming_data, key))
            result['message'] = "Params content Error: cant't find key=%s" % (key)
            return json.dumps(result)

    logger.info('[log.rawsenz] valid request with params=%s' %(incoming_data))

    try:
        result['result'] = collect_senz_lists(incoming_data)
        result['code'] = 0
        result['message'] = 'success'
    except Exception, e:
        logger.exception('[Exception] generate result error: %s' % (str(e)))
        result['code'] = 1
        result['message'] = '500 Internal Error'
        return json.dumps(result)

    return json.dumps(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=9010)
