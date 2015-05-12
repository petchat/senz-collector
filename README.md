SENZ COLLECTOR
===

# What can I use this for?
It used to collect senz tuple from discrete timestamp seqs which include motion, sound, location and so on.
eg. senz tuple look like:
```
{
    "motion":   {"timestamp": "2015-03-18 05:49:04", ...},
    "location": {"timestamp": "2015-03-18 05:49:10", ...},
    "sound":    {"timestamp": "2015-03-18 05:49:05", ...}
}
```
You should input object lists(the object contains key 'timestamp') into SenzCollector, and select a key as primary key.
Also you could set a filter to discard some tuple which timestamp delta is too much.
The algo will output a list of senz object,and their timestamp group which other key's timestamp is closet to the primary key's timestamp.
So the timestamp of every item's primary key in the output list is consequent.

# How to use it?
- Input
*time_lines* is a dict, and it can contain more than one timestamp sequences.
Every sequence also is a dict, key is the name of time line, and value is a list which contains timestamp seqs.
Key can be any word. The selected key will be *primary key* which clustering algo based on.
```
{
    "timelines": {
        "key 0": [{"timestamp": key0_timestamp0, ...}, {"timestamp": key0_timestamp1, ...}, ...],
        "key 1": [{"timestamp": key1_timestamp0, ...}, {"timestamp": key1_timestamp1, ...}, ...],
        "key 2": [{"timestamp": key2_timestamp0, ...}, {"timestamp": key2_timestamp1, ...}, ...]
    }
    "filter": setting value
    "primaryKey": "key 0"
}
```
- Output
Return value is a list, the item of return list is a dict which contains N sub-dict( key: key_timestamp ).
```
[
    {
        "senzTimestamp": key0_timestamp0,
        "key0": {"timestamp": key0_timestamp0, ...},
        "key1": {"timestamp": key1_timestamp1, ...},
        "key2": {"timestamp": key2_timestamp0, ...},
        ...
    },
    ...
]
```

# Example
You can invoke this module directly in python.
```python
import senz_collector

input_data = {"filter":1,"key0":[{"timestamp": 2},{"timestamp": 4},{"timestamp": 6},{"timestamp": 9}],"key1":[{"timestamp": 3},{"timestamp": 4},{"timestamp": 7},{"timestamp": 9}],"key2":[{"timestamp": 1},{"timestamp": 3},{"timestamp": 6}],"primaryKey":"key0"}
senz_collector.SenzCollector(input_data)
```
Also you can use it in shell.
```shell
python senz_collector.py '{"filter":1,"key0":[{"timestamp": 2},{"timestamp": 4},{"timestamp": 6},{"timestamp": 9}],"key1":[{"timestamp": 3},{"timestamp": 4},{"timestamp": 7},{"timestamp": 9}],"key2":[{"timestamp": 1},{"timestamp": 3},{"timestamp": 6}],"primaryKey":"key0"}'
```
Mostly, you need call it as a restful api. It offers a 'post' interface.

# Warning
Integer timestamp(like unixtime) is strongly recommended.