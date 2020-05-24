from django.core.management.base import BaseCommand
import json


class Command(BaseCommand):
    help = 'Read Json File'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='Indicates the file name')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        location = 'Sample Input Files/' + file_name + '.json'
        with open(location) as f:
            data = json.load(f)
        print(len(data))
        for i in range(len(data)):
            for key, value in data[i].items():
                print(key, value)


