import threading
import json
import redis
from faker import Faker
from datetime import datetime
from rejson import Client, Path
from random import randrange


bad = False


def create_data():
    fake = Faker('nl_NL')
    string0 = fake.uri()
    string1 = fake.date_time().isoformat()
    string2 = fake.word()
    string3 = fake.address().splitlines()[1]
    string4 = fake.text(max_nb_chars=40)
    string5 = fake.random_int()
    string6 = fake.uuid4()
    strings = [string0, string1, string2, string3, string4, string5, string6]
    return strings


def create_bad_data():
    random = randrange(6)
    fake = Faker('nl_NL')
    string0 = 'http://baddata.org/main/'
    string1 = fake.date_time().isoformat()
    string2 = fake.word()
    string3 = fake.address().splitlines()[1]
    string4 = fake.text(max_nb_chars=40)
    string5 = fake.random_int()
    string6 = 'ec72ba0b-948a-446d-aed9-9cd2eab9011d'
    strings = [string0, string1, string2, string3, string4, string5, string6]
    strings[random] = None
    return strings


def print_data(data):
    for key, value in data.items():
        print(key, value)


def create_json(strings):
    item = {'String0': strings[0],
            'String1': strings[1],
            'String2': strings[2],
            'String3': strings[3],
            'String4': strings[4],
            'String5': strings[5],
            'String6': strings[6],
            'created': datetime.now().isoformat(),
            'historyData': []}
    json_item = json.dumps(item)
    data = json.loads(json_item)
    return data


def inject_data():
    # i as interval in seconds
    n = 5
    threading.Timer(n, inject_data).start()
    # gets executed every n seconds
    if bad:
        strings = create_bad_data()
    else:
        strings = create_data()
    item = create_json(strings)
    print_data(item)
    # create redis queue and store data
    grading_queue = redis.StrictRedis('localhost', 6379)
    key = strings[6]
    print('Injecting item to pre-processing queue')
    grading_queue.execute_command('JSON.SET', key, '.', json.dumps(item))


def main():
    global bad
    print("Enter 1 for complete data and 0 for incomplete data: ")
    bad = int(input())
    if bad > 0:
        bad = False
    else:
        bad = True
    inject_data()


if __name__ == "__main__":
    main()

