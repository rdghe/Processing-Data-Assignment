import xmltodict
import json
from django.core.management.base import BaseCommand
from xml.dom import minidom


def to_dict(input_ordered_dict):
    return json.loads(json.dumps(input_ordered_dict))


class Command(BaseCommand):
    help = 'Read XML File'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='Indicates the file name')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        location = 'Sample Input Files/' + file_name + '.xml'

        with open(location) as f:
            data = xmltodict.parse(f.read())
            json.dumps(data)
            data = to_dict(data)
            print(data)
            for i in range(len(data)):
                for key, value in data[i].items():
                    print(key, value)


