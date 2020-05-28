import redis
import json
import xmltodict
from xml.etree import ElementTree
from collections import OrderedDict


def to_dict(input_ordered_dict):
    return json.loads(json.dumps(input_ordered_dict))


def read_xml_file(xml_file):
    with open(xml_file) as f:
        data = xmltodict.parse(f.read())
        json.dumps(data)
        data = to_dict(data)
        key = list(data.keys())[0]
        data = data[key]
        # this needs to be fixed later because it doesn't fork for input-sample2
        key = list(data.keys())[0]
        data = data[key]
        return data


def read_json_file(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data


input_files = ['Sample Input Files/input-sample1.xml', 'Sample Input Files/input-sample3.json']
# , 'Sample Input Files/input-sample2.xml']


for file in input_files:
    if file.endswith('.xml'):
        xml_data = read_xml_file(file)
        for i in range(len(xml_data)):
            print(xml_data[i])

    elif file.endswith('.json'):
        json_data = read_json_file(file)
        for i in range(len(json_data)):
            print(json_data[i])

# r = redis.StrictRedis()
# r.execute_command('JSON.SET', 'doc', '.', json.dumps(data))
# reply = json.loads(r.execute_command('JSON.GET', 'doc'))
