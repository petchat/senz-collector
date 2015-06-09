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

logger.info("[log.rawsenz] Start...")

app = Flask(__name__)


@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init('6b773c84e86041798a513ba8ef73bb74',
                 'petchat-flask',
                 root=os.path.dirname(os.path.realpath(__file__)),
                 allow_logging_basic_config=False)

    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


@app.route('/', methods=['POST'])
def senzCollectorAPI():
    result = {'code': 1, 'message': ''}

    # params JSON validate
    try:
        incoming_data = json.loads(request.data)
    except ValueError, err_msg:
        logger.error('[ValueError] err_msg: %s, params=%s' % (err_msg, request.data))
        result['message'] = 'Unvalid params: NOT a JSON Object'
        return json.dumps(result)

    # params key checking
    for key in ['filter', 'timelines']:
        if key not in incoming_data:
            logger.error("[KeyError] params=%s, should have key: %s" % (incoming_data, key))
            result['message'] = "Params content Error: cant't find key=%s" % (key)
            return json.dumps(result)

    try:
        result['result'] = collect_senz_lists(incoming_data)
        result['code'] = 0
        result['message'] = 'success'
    except Exception, e:
        logger.error('[Exception] generate result error: %s' % (str(e)))
        result['code'] = 1
        result['message'] = '500 Internal Error'
        return json.dumps(result)

    return json.dumps(result)

if __name__ == '__main__':
    app.debug = True
    app.run(port=9009)
