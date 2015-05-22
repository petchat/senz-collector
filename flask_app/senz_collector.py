# -*- coding: UTF-8 -*-
__author__ = 'woodie'

import sys
import json

def SenzCollector(input_data):
    '''
    SENZ COLLECTOR

    It used to collect senz tuple from discrete timestamp seqs which include motion, sound, location and so on.
        eg. senz tuple look like:
            {
                "motion":   2015-03-18 05:49:04,
                "location": 2015-03-18 05:49:10,
                "sound":    2015-03-18 05:49:05
            }
    You should input timestamp lists into SenzCollector, and select a key as primary key.
    The algo will output a list of timestamp group which other key's timestamp is closet to the primary key's timestamp.
    So the timestamp of every item's primary key in the output list is consequent.


    :param time_lines:
        *time_lines* is a dict, and it can contain more than one timestamp sequences.
        Every sequence also is a dict, key is the name of time line, and value is a list which contains timestamp seqs.
        Key can be any word. The selected key will be *primary key* which clustering algo based on.
        eg. {
                "filter"
                "timelines": {
                    "key 0": [key0_timestamp0, key0_timestamp1, ...],
                    "key 1": [key1_timestamp0, key1_timestamp1, ...],
                    "key 2": [key2_timestamp0, key2_timestamp1, ...],
                    ...
                }
                "primaryKey": "key 0"
            }
    :return:
        Return value is a list, the item of return list is a dict which contains N sub-dict( key: key_timestamp ).
        eg. [
                {
                    "senzTimestamp": key0_timestamp0,
                    "key0": key0_timestamp0,
                    "key1": key1_timestamp1,
                    "key2": key2_timestamp0,
                    ...
                },
                ...
            ]
    '''
    filter = 2
    if input_data.has_key("filter"):
        filter = input_data.pop("filter")
    # If there is primary key,
    # then get the primary key, and remove the primary key from input.
    if input_data.has_key("primaryKey"):
        primary_key = input_data.pop("primaryKey")
        timelines = SupplyDeficiency(primary_key, input_data)
        return SenzFilter(ClusteringBaseOnPrimaryKey(primary_key, timelines), filter)
    # If there is no primary key,
    # then it will clutering decentralized.
    return SenzFilter(ClusteringDecentralized(input_data), filter)

def SupplyDeficiency(primary_key, timelines):
    _timelines = timelines
    if len(_timelines[primary_key]) <= 0:
        return None
    for (key, timeline) in _timelines.items():
        if key != primary_key and len(timeline) <= 0:
            # Create counterfeit according to primary key timeline
            normal_timeline = []
            for primary_object in _timelines[primary_key]:
                normal_object = {
                    "objectId": "counterfeitObjectId",
                    "userRawdataId": "counterfeitRawdataId",
                    "timestamp": primary_object["timestamp"]
                }
                normal_timeline.append(normal_object)
            _timelines[key] = normal_timeline
    return _timelines


def ClusteringBaseOnPrimaryKey(primary_key, time_lines):
    result_list = []
    # Scan the primary key list's timestamp one by one.
    for primary_object in time_lines.pop(primary_key):
        senz_tuple = {primary_key: primary_object}
        # Select the closest timestamp to primary key timestamp in different time line
        for (key, time_line) in time_lines.items():
            min_delta     = 99999999999999
            closet_object = {}
            # Compare every timestamp with primary key timestamp in time line.
            for normal_object in time_line:
                if abs(int(primary_object['timestamp']) - int(normal_object['timestamp'])) < min_delta:
                    min_delta     = abs(int(primary_object['timestamp']) - int(normal_object['timestamp']))
                    closet_object = normal_object
                else:
                    break
            senz_tuple[key] = closet_object
        result_list.append(senz_tuple)
    return result_list


def ClusteringDecentralized(time_lines):
    return []



def SenzFilter(tuple_list, filter):
    return_tuple_list = []
    print 'The tuple list len is:', len(tuple_list)
    print 'The setting variance is:', pow(int(filter), 2)
    for tuple in tuple_list:
        print 'Senz Tuple is:\n', tuple
        # Expectation of timestamps in a tuple
        expectation = 0
        for obj in tuple.values():
            expectation += obj['timestamp']
        expectation /= len(tuple)
        print 'E =', expectation
        # Variance Square of timestamps in a tuple
        variance_square = 0
        for obj in tuple.values():
            variance_square += pow(obj['timestamp'] - expectation, 2)
        print 'D =', variance_square
        # Filtering
        if variance_square < pow(int(filter), 2):
            # tuple_list.remove(tuple)
            return_tuple_list.append(tuple)
    print 'Return Tuple List is:', return_tuple_list
    print 'The len of it is:', len(return_tuple_list)
    return return_tuple_list



if __name__ == "__main__":

    # if len(sys.argv) >= 2:
    #     input_data = json.loads(sys.argv[1])
    #     print SenzCollector(input_data)
    # else:
    #     print "Input data is needed."
    data = {
        "filter": 100,
        "key0": [{'timestamp': 2}, {'timestamp': 4}, {'timestamp': 6}, {'timestamp': 9}],
        "key1": [{'timestamp': 3}, {'timestamp': 4}, {'timestamp': 7}, {'timestamp': 9}],
        "key2": [],
        "primaryKey": "key0"
    }

    print SenzCollector(data)

    # data2 = {
    #     "key0": [{'timestamp': 2}, {'timestamp': 4}, {'timestamp': 6}, {'timestamp': 9}],
    #     "key1": [],
    #     "key2": [{'timestamp': 1}, {'timestamp': 3}, {'timestamp': 6}],
    #     "key3": [{'timestamp': 1}, {'timestamp': 3}, {'timestamp': 6}]
    # }

    # print SupplyDeficiency("key0", data2)

# {
#     "filter": 1,
#     "key0":   [2, 4, 6, 9],
#     "key1":   [3, 4, 7, 9],
#     "key2":   [1, 3, 6],
#     "primaryKey": "key0"
# }
