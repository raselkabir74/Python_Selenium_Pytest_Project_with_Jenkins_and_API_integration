import json
import time
import uuid
from urllib.parse import urlparse

import requests
import os
from configurations import configurations
from datetime import datetime
from . import secrets

config = configurations.load_config_by_usertype()

BASE_URL = config['credential']['url']

username = config['credential']['username']
passphrase = config['credential']['password']

driver = None

step = 0

DELAY = 25

MYSQL_MAX_RETRY = int(config['mysql']['max-retry'])
MYSQL_WAIT_TIME = int(config['mysql']['wait'])
ONE_MINUTE_DELAY = int(config['wait']['one-minute'])
HALF_MINUTE_DELAY = int(config['wait']['half-minute'])
SHORT_DELAY = int(config['wait']['short-delay'])
FIVE_SEC_DELAY = int(config['wait']['five-sec-delay'])
ONE_SEC_DELAY = int(config['wait']['one-sec-delay'])


def get_api_access_token(end_point, credential, user_type="admin"):
    if 'dsp-qa-testing' in config['credential']['url']:
        base_url = config['credential']['api-url'].format('dsp-qa-testing')
    elif 'dsp.eskimi.com' in config['credential']['url']:
        base_url = config['credential']['api-url'].format('dsp')
    else:
        url = config['credential']['url']
        start_pos = url.find("dsp")
        end_pos = url.find(".", start_pos)
        stage = url[start_pos:end_pos]
        base_url = config['credential']['api-url'].format(stage)
    max_attempts = 30
    attempts = 0
    while attempts < max_attempts:
        try:
            payload = {}
            if user_type == "admin":
                payload = {
                    'grant_type': 'eskimi_dsp',
                    'username': credential['username'],
                    'password': credential['password'],
                    'client_id': int(credential['client-id']),
                    'client_secret': credential['client-secret']
                }
            elif user_type == "agency-client":
                payload = {
                    'grant_type': 'eskimi_dsp',
                    'username': credential['agency-client-username'],
                    'password': credential['agency-client-password'],
                    'client_id': int(credential['agency-client-client-id']),
                    'client_secret': credential['agency-client-client-secret']
                }
            headers = {'content-type': 'application/json'}
            response = json.loads(
                requests.request('POST', '{}{}'.format(base_url, end_point),
                                 data=json.dumps(payload),
                                 headers=headers).text)
            return response['access_token'], base_url, config
        except Exception as e:
            print("Error occurred:", e)
            attempts += 1
            if attempts < max_attempts:
                print("Retrying...")
                time.sleep(1)
    print("Maximum attempts reached. Unable to get API access token.")
    return None, None


def get_random_string(length=10):
    return uuid.uuid4().hex[:length]


def step_printer(stepstr):
    global step
    if step == 0:
        step = step + 1
        print('\nStep {} --> {}'.format(step, stepstr))
    else:
        step = step + 1
        print('Step {} --> {}'.format(step, stepstr))


def step_info(info):
    print(info)


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def time_within_range(start=6, end=10, x=int(datetime.now().strftime("%H"))):
    print(x)
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
