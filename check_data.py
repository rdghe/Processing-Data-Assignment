import threading
import json
import redis
import re
from dateutil.parser import parse
from rejson import Client, Path


def print_data(data):
    for key, value in data.items():
        print(key, value)


def validate_url(data):
    if not data:
        return 'F'
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, data) is not None:
        return 'A'
    else:
        return 'D'


def validate_date_time(data):
    if not data:
        return 'F'
    try:
        parse(data)
        return 'A'
    except ValueError:
        return 'C'


def validate_category(data):
    if not data:
        return 'B'
    if isinstance(data, str):
        return 'A'
    else:
        return 'B'


def validate_postcode(data):
    if not data:
        return 'F'
    regex = re.compile('[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[A-Za-z][ ]*[A-Za-z]')
    if re.match(regex, data) is not None:
        return 'A'
    else:
        return 'D'


def validate_string(data):
    print(data)
    if not data:
        return 'B'
    if isinstance(data, str) and 4 < len(data) < 51:
        return 'A'
    else:
        return 'B'


def check_data(data):
    string0_grade = validate_url(data['String0'])
    string1_grade = validate_date_time(data['String1'])
    string2_grade = validate_category(data['String2'])
    string3_grade = validate_postcode(data['String3'])
    string4_grade = validate_string(data['String4'])

    grades = [string0_grade, string1_grade, string2_grade, string3_grade, string4_grade]
    print(grades)



def retrieve_and_check():
    # i as interval in seconds
    n = 5
    threading.Timer(n, retrieve_and_check).start()

    # gets executed every n seconds
    # retrieve data from redis and print it
    r = redis.StrictRedis('localhost', 6379)
    item = json.loads(r.execute_command('JSON.GET', 'object'))

    print_data(item)
    # check_data(item)


def main():
    retrieve_and_check()


if __name__ == "__main__":
    main()
