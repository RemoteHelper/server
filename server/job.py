#!/usr/bin/env python3


class Job:
    def __init__(self):
        self._completed = False

    def complete_job(self):
        self._completed = True

    def is_complete(self):
        return self._completed
