# -*- coding: UTF-8 -*-
__author__ = 'woodie'

from flask import Flask, request, url_for, Response, send_file
from senz_collector import SenzCollector
import json
# import yaml
# import json



app = Flask(__name__)

@app.route('/', methods=['POST'])
def senzCollectorAPI():
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
        print 'Received filter is', filter, ', and primary key is', primaryKey
        print 'The input data content is'
        print data
        result = json.dumps({'result': SenzCollector(data)})
    return result

if __name__ == '__main__':
    app.debug = True
    app.run(port=9009)
