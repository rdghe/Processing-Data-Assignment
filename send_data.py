import redis
import json
import xmltodict
from xml.etree import ElementTree
from collections import OrderedDict


def to_dict(input_ordered_dict):
    return json.loads(json.dumps(input_ordered_dict))


# r = redis.StrictRedis()
# r.execute_command('JSON.SET', 'doc', '.', json.dumps(data))
# reply = json.loads(r.execute_command('JSON.GET', 'doc'))

xml_files = ['Sample Input Files/input-sample1.xml', 'Sample Input Files/input-sample2.xml']

for file in xml_files:
    with open(file) as f:
        data = xmltodict.parse(f.read())
        json.dumps(data)
        data = to_dict(data)
        print(data)
        # for i in range(len(data)):
        #     for key, value in data[i].items():
        #         print(key, value)

json_files = ['Sample Input Files/input-sample3.json']
for file_name in json_files:
    with open(file_name) as f:
        data = json.load(f)
    print(len(data))
    print(data)
    # for i in range(len(data)):
    #     for key, value in data[i].items():
    #         print(key, value)
