import redis
import json
import xmltodict
import re
import datetime
from xml.etree import ElementTree
from collections import OrderedDict
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class Data:
    def __init__(self, url, date_time, category, postal_code, string, integer, id_string):
        self.url = url
        self.date_time = date_time
        self.category = category
        self.postal_code = postal_code
        self.string = string
        self.integer = integer
        self.id_string = id_string
        self.grade = 'A'

    def grade_if_missing(self):
        if not (self.url and self.date_time and self.postal_code):
            self.grade = 'F'
        if not (self.category and self.string and self.integer):
            self.grade = 'B'

    def validate_url(self):
        val = URLValidator(verify_exists=False)
        try:
            val(self.url)
        except ValidationError as e:
            print(e)
            self.grade = 'D'

    def validate_date_time(self):
        r = re.compile('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}')
        if r.match(self.date_time) is None:
            print('Not a date and/or time')

    def print_data(self):
        print('String0: ' + str(self.url))
        print('String1: ' + str(self.date_time))
        print('String2: ' + str(self.category))
        print('String3: ' + str(self.postal_code))
        print('String4: ' + str(self.string))
        print('String5: ' + str(self.integer))
        print('String6 ' + str(self.id_string))
        print('Grade: ' + str(self.grade))


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


def validate_and_grade(data):
    url = list(data.values())[0]
    date_time = list(data.values())[1]
    category = list(data.values())[2]
    postal_code = list(data.values())[3]
    string = list(data.values())[4]
    integer = list(data.values())[5]
    id_string = list(data.values())[6]

    data_item = Data(url, date_time, category, postal_code, string, integer, id_string)
    data_item.grade_if_missing()
    data_item.print_data()


for file in input_files:
    if file.endswith('.xml'):
        xml_data = read_xml_file(file)
        for i in range(len(xml_data)):
            # print(xml_data[i])
            validate_and_grade(xml_data[i])
    elif file.endswith('.json'):
        json_data = read_json_file(file)
        for i in range(len(json_data)):
            # print(json_data[i])
            validate_and_grade(json_data[i])
