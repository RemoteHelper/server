#!/usr/bin/env python3

import json


# -> URL
def _get_complete_url():
    host = config['host']
    return host['protocol'] + host['url'] + ':' + str(host['port'])


# -> URL
def get_done_url():
    return _get_complete_url() + config['done_endpoint']


# -> String
def get_domain_name():
    return config['host']['url']


# -> String
def get_domain_port():
    return config['host']['port']


# -> URL
def get_user_endpoint():
    return _get_complete_url() + config['user_endpoint']

with open('config.json', 'r') as conf:
    config = json.load(conf)