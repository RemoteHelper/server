#!/usr/bin/env python3


class Job:
    def __init__(self, events_url):
        self._completed = False
        self._events_url = events_url

    def complete_job(self):
        self._events_url = None
        self._completed = True

    def is_complete(self):
        return self._completed

    def get_events_url(self):
        return self._events_url
