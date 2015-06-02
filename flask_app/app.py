# -*- coding: UTF-8 -*-
__author__ = 'woodie'

from flask import Flask, request
from senz_collector import SenzCollector
import json
from logger import logger

logger.info("[log.rawsenz] Start...")

app = Flask(__name__)

@app.route('/', methods=['POST'])
def senzCollectorAPI():
    # TODO: apply new strategy
    result = 'Your request is illegal'
    if request.method == 'POST':
        incoming_data = json.loads(request.data)
        filter     = incoming_data['filter']
        primaryKey = incoming_data['primary_key']
        # print incoming_data['timelines']
        timelines  = incoming_data['timelines']
        data = {
            'filter': filter,
            'primaryKey': primaryKey
        }
        for (key, timeline) in timelines.items():
            data[key] = timeline
        logger.info('[API] Received filter is', filter, ', and primary key is', primaryKey)
        logger.info('[API] The input data content is')
        logger.info('[API] data: ', data)
        result = json.dumps({'result': SenzCollector(data)})
    return result

if __name__ == '__main__':
    app.debug = True
    app.run(port=9009)
