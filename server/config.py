#!/usr/bin/env python3

import json


class Config:
    def __init__(self, config_file):
        with open(config_file, 'r') as conf:
            self._config = json.load(conf)

    # -> URL
    def __get_complete_url(self):
        host = self._config['host']
        return host['protocol'] + host['url'] + ':' + str(host['port'])

    # -> URL
    def get_done_url(self):
        return self.__get_complete_url() + self._config['done_endpoint']

    # -> String
    def get_domain_name(self):
        return self._config['host']['url']

    # -> String
    def get_domain_port(self):
        return self._config['host']['port']

    # -> URL
    def get_user_endpoint(self):
        return self.__get_complete_url() + self._config['user_endpoint']
