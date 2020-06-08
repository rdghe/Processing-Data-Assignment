import threading
import json
import redis
import re
from rejson import Client, Path


def print_data(data):
    for key, value in data.items():
        print(key, value)


def dedup_data():
    # i as interval in seconds
    n = 5
    threading.Timer(n, dedup_data).start()

    # gets executed every n seconds
    # retrieve a RANDOM data point from the redis queue
    grading_queue = redis.StrictRedis('localhost', 6380)
    key = grading_queue.randomkey()
    item = json.loads(grading_queue.execute_command('JSON.GET', key))
    print_data(item)


def main():
    dedup_data()


if __name__ == "__main__":
    main()