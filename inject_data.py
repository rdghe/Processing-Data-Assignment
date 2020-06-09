import threading
import json
import redis
from faker import Faker
from datetime import datetime
from rejson import Client, Path


def create_data():
    fake = Faker('nl_NL')
    string0 = fake.uri()
    string1 = fake.date_time().strftime("%m/%d/%Y, %H:%M:%S")
    string2 = fake.word()
    string3 = fake.address().splitlines()[1]
    string4 = fake.text(max_nb_chars=40)
    string5 = fake.random_int()
    string6 = fake.uuid4()
    strings = [string0, string1, string2, string3, string4, string5, string6]
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
            'created': datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    json_item = json.dumps(item)
    data = json.loads(json_item)
    return data


def inject_data():
    # i as interval in seconds
    n = 5
    threading.Timer(n, inject_data).start()

    # gets executed every n seconds
    strings = create_data()
    item = create_json(strings)

    # create redis queue and store data
    grading_queue = redis.StrictRedis('localhost', 6379)
    # print_data(item)
    key = strings[6]
    grading_queue.execute_command('JSON.SET', key, '.', json.dumps(item))


def main():
    inject_data()


if __name__ == "__main__":
    main()

