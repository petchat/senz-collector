# -*- coding: UTF-8 -*-
__author__ = 'woodie'

from flask import Flask, request, got_request_exception
# from senz_collector import SenzCollector
import json
import os
from logger import logger
import rollbar
import rollbar.contrib.flask

from timesequence_align import collect_senz_lists
from config import *

logger.info("[log.rawsenz] Start...")

app = Flask(__name__)


@app.before_first_request
def init_rollbar():
    import datetime

    init_tag = "[Initiation of Service Process]\n"

    """init rollbar module"""
    rollbar.init(ROLLBAR_TOKEN,
                 APP_ENV,
                 root=os.path.dirname(os.path.realpath(__file__)),
                 allow_logging_basic_config=False)

    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

    log_init_time = "Initiation START at: \t%s\n" % datetime.datetime.now()
    log_app_env = "Environment Variable: \t%s\n" % APP_ENV
    log_rollbar_token = "Rollbar Service TOKEN: \t%s\n" % ROLLBAR_TOKEN
    log_logentries_token = "Logentries Service TOKEN: \t%s\n" % LOGENTRIES_TOKEN
    logger.info(init_tag + log_init_time)
    logger.info(init_tag + log_app_env)
    logger.info(init_tag + log_rollbar_token)
    logger.info(init_tag + log_logentries_token)


@app.route('/', methods=['POST'])
def senzCollectorAPI():
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
