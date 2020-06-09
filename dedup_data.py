import json
import redis


def print_data(data):
    for key, value in data.items():
        print(key, value)


def merge_data(key, item, old_item):
    counter = 0
    if item['grades'] == ['A', 'A', 'A', 'A', 'A', 'A']:
        item['status'] = 1
    for i in range(len(item['grades'])):
        if item['grades'][i] > old_item['grades'][i]:
            counter += 1
            key_ = 'String' + str(i)
            item[key_] = old_item[key_]
            item['grades'][i] = old_item['grades'][i]
            old_item['status'] = -1
    if counter > 0 and item['status'] < 1:
        if 'historyData' not in item:
            item['historyData'] = [old_item]
        else:
            item['historyData'].append(old_item)

        dedup_queue = redis.StrictRedis('localhost', 6380)
        dedup_queue.execute_command('JSON.SET', key, '.', json.dumps(item))
        print(old_item)
        print(item['historyData'])


def deduplicate_data(key, item):
    dedup_queue = redis.StrictRedis('localhost', 6380)
    exists = dedup_queue.execute_command('EXISTS', key)
    if exists > 0:
        print('Extracting item from queue.')
        old_item = json.loads(dedup_queue.execute_command('JSON.GET', key))
        merge_data(key, item, old_item)
    else:
        print('Item not found in queue. Placing it now.')
        item['historyData'] = []
        dedup_queue.execute_command('JSON.SET', key, '.', json.dumps(item))
