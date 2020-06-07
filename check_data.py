import threading
import json
import redis
from rejson import Client, Path


def print_data(data):
    for key, value in data.items():
        print(key, value)


def check_data():
    # i as interval in seconds
    n = 10
    threading.Timer(n, check_data).start()

    # gets executed every n seconds
    # retrieve data from redis and print it
    r = redis.StrictRedis('localhost', 6379)
    item = json.loads(r.execute_command('JSON.GET', 'object'))
    print_data(item)


def main():
    check_data()


if __name__ == "__main__":
    main()
