import threading
import json
import redis
import re
import math
from dateutil.parser import parse
from rejson import Client, Path
import dedup_data


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
    if not data:
        return 'B'
    if isinstance(data, str) and 4 < len(data) < 51:
        return 'A'
    else:
        return 'B'


def validate_integer(data):
    if not data:
        return 'B'
    frac, whole = math.modf(data)
    if isinstance(data, int) or (isinstance(data, float) and frac == 0):
        return 'A'
    else:
        return 'B'


def compute_grade(grades):
    if 'F' in grades:
        return 'F'
    elif 'D' in grades:
        return 'D'
    elif 'C' in grades:
        return 'C'
    elif 'B' in grades:
        return 'B'
    else:
        return 'A'


def grade_data(data):
    string0_grade = validate_url(data['String0'])
    string1_grade = validate_date_time(data['String1'])
    string2_grade = validate_category(data['String2'])
    string3_grade = validate_postcode(data['String3'])
    string4_grade = validate_string(data['String4'])
    string5_grade = validate_integer(data['String5'])
    grades = [string0_grade, string1_grade, string2_grade, string3_grade, string4_grade, string5_grade]
    grade = compute_grade(grades)
    data['grades'] = grades
    return data


def retrieve_and_check():
    # i as interval in seconds
    n = 5
    threading.Timer(n, retrieve_and_check).start()

    # gets executed every n seconds
    # retrieve a RANDOM data point from the redis queue
    grading_queue = redis.StrictRedis('localhost', 6379)
    key = grading_queue.randomkey()
    if key is None:
        print('Pre-processing queue is empty.')
        return
    item = json.loads(grading_queue.execute_command('JSON.GET', key))
    item = grade_data(item)
    if item['grades'] == ['A', 'A', 'A', 'A', 'A', 'A']:
        item['status'] = 1
    else:
        item['status'] = 0
    # delete item from redis queue
    grading_queue.execute_command('JSON.DEL', key)

    # forward item to de-duplication queue
    dedup_data.deduplicate_data(key, item)


def main():
    retrieve_and_check()


if __name__ == "__main__":
    main()
