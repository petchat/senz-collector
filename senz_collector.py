__author__ = 'woodie'

def SenzCollector(**time_lines):
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
                "key 0": [key0_timestamp0, key0_timestamp1, ...],
                "key 1": [key1_timestamp0, key1_timestamp1, ...],
                "key 2": [key2_timestamp0, key2_timestamp1, ...],
                ...
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
    # If there is primary key
    # then get the primary key, and remove the primary key from input.
    if time_lines.has_key("primaryKey"):
        primary_key = time_lines.pop("primaryKey")
        return ClusteringBaseOnPrimaryKey(primary_key, time_lines)

    return ClusteringDecentralized(time_lines)


def ClusteringBaseOnPrimaryKey(primary_key, time_lines):
    result_list = []
    # Scan the primary key list's timestamp one by one.
    for primary_timestamp in time_lines.pop(primary_key):
        # Select the closest timestamp to primary key timestamp in different time line
        senz_tuple = {primary_key: primary_timestamp}
        for (key, time_line) in time_lines.items():
            min_delta = 99999999999
            # Compare every timestamp with primary key timestamp in time line.
            for normal_timestamp in time_line:
                if abs(primary_timestamp - normal_timestamp) < min_delta:
                    min_delta = abs(primary_timestamp - normal_timestamp)
                else:
                    break
            senz_tuple[key] = normal_timestamp
        result_list.append(senz_tuple)
    return result_list


def ClusteringDecentralized(time_lines):
    return []

if __name__ == "__main__":
    print SenzCollector(key0=[1,2,3], key1=[1,2,3], key2=[1,2,3], primaryKey="key0")