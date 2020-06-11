from django.core.management.base import BaseCommand
from application.models import CurrentData, HistoryData, SyncItem, SyncBag
import json
import redis
from check_data import compute_grade


class Command(BaseCommand):
    help = 'Store data from queue into the Database'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        queue = redis.StrictRedis('localhost', 6380)
        key = queue.randomkey()
        if key is None:
            print('Queue is empty')
            return
        print('Creating SyncBag')
        sync_bag = SyncBag.objects.create()
        while True:
            key = queue.randomkey()
            if key is None:
                print('No more items in queue')
                return  # set as 'continue' for continuous running
            item = json.loads(queue.execute_command('JSON.GET', key))
            print('Key ' + str(key) + ' extracted from Redis queue')

            print('Creating SyncItem')
            sync_item = SyncItem.objects.create(syncBag=sync_bag, grade=compute_grade(item['grades']))
            print('Creating CurrentData')
            current_data = CurrentData.objects.create(id_dataString6=item['String6'], status=item['status'],
                                                      created=item['created'], dataString0=item['String0'],
                                                      dataString1=item['String1'], dataString2=item['String2'],
                                                      dataString3=item['String3'], dataString4=item['String4'],
                                                      dataString5=item['String5'], syncItem=sync_item)
            for data in item['historyData']:
                print('Creating HistoryData')
                history_data = HistoryData.objects.create(id_dataString6=data['String6'], status=data['status'],
                                                          created=data['created'], dataString0=data['String0'],
                                                          dataString1=data['String1'], dataString2=data['String2'],
                                                          dataString3=data['String3'], dataString4=data['String4'],
                                                          dataString5=data['String5'], syncItem=sync_item)
            print('Deleting item from queue')
            queue.execute_command('JSON.DEL', key)
