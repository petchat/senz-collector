# -*- coding: UTF-8 -*-

"""Unit test for app.py"""

__author__ = 'jiaying.lu'

from unittest import TestCase
from flask_app.app import app
import json

class TestSenzCollectorAPI(TestCase):

    def setUp(self):
        super(TestSenzCollectorAPI, self).setUp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        super(TestSenzCollectorAPI, self).tearDown()
        app.config['TESTING'] = False

    def test_empty_params(self):
        rv = self.app.post('/', data='')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(1, result['code'])

    def test_unvalid_params(self):
        rv = self.app.post('/', data='OhMyParams')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(1, result['code'])

    def test_valid_params(self):
        data = {
            'primary_key': 'HK',
            'filter': 1,
            'timelines': {
                'PK': [{'timestamp': 1}, {'timestamp': 3}, {'timestamp': 5}],
                'SK': []
            }
        }
        rv = self.app.post('/', data=json.dumps(data))
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(0, result['code'])
        senz_collected = [
            {'SK': {'timestamp': 1, 'objectId': 'counterfeitObjectId', 'userRawdataId': 'counterfeitRawdataId'},
             'PK': {'timestamp': 1}},
            {'SK': {'timestamp': 3, 'objectId': 'counterfeitObjectId', 'userRawdataId': 'counterfeitRawdataId'},
             'PK': {'timestamp': 3}},
            {'SK': {'timestamp': 5, 'objectId': 'counterfeitObjectId', 'userRawdataId': 'counterfeitRawdataId'},
             'PK': {'timestamp': 5}}]
        self.assertEqual(senz_collected, result['result'])
