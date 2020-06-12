import json
import redis


def print_data(data):
    for key, value in data.items():
        print(key, value)


def merge_data(key, item, old_item):
    counter = 0
    dedup_queue = redis.StrictRedis('localhost', 6380)
    if item['grades'] == ['A', 'A', 'A', 'A', 'A', 'A']:
        item['status'] = 1
        old_item['status'] = -1
        item['historyData'].append(old_item['historyData'])
        del old_item['historyData']
        del old_item['grades']
        item['historyData'].append(old_item)
        dedup_queue.execute_command('JSON.SET', key, '.', json.dumps(item))
        return
    for i in range(len(item['grades'])):
        if item['grades'][i] > old_item['grades'][i]:
            counter += 1
            key_ = 'String' + str(i)
            item[key_] = old_item[key_]
            item['grades'][i] = old_item['grades'][i]
    if counter > 0:
        old_item['status'] = -1
        item['historyData'] += (old_item['historyData'])
        del old_item['historyData']
        del old_item['grades']
        item['historyData'].append(old_item)
        if item['grades'] == ['A', 'A', 'A', 'A', 'A', 'A']:
            item['status'] = 1
        dedup_queue.execute_command('JSON.SET', key, '.', json.dumps(item))
        print(item)


def deduplicate_data(key, item):
    dedup_queue = redis.StrictRedis('localhost', 6380)
    exists = dedup_queue.execute_command('EXISTS', key)
    if exists > 0:
        print('Extracting item from queue. De-duplicating..')
        old_item = json.loads(dedup_queue.execute_command('JSON.GET', key))
        merge_data(key, item, old_item)
    else:
        print('Item not found in queue. Placing it now.')
        dedup_queue.execute_command('JSON.SET', key, '.', json.dumps(item))
