from django.core.management.base import BaseCommand
from xml.dom import minidom


class Command(BaseCommand):
    help = 'Read Json File'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='Indicates the file name')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        location = 'Sample Input Files/' + file_name + '.xml'

        xml_doc = minidom.parse(location)
        item_list = xml_doc.getElementsByTagName('String0')
        print(item_list)
        # print(item_list[0].attributes['string0'].value)
        # for s in item_list:
        #     print(s.attributes['name'].value)


