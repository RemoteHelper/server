#!/usr/bin/env python3

import uuid


class Storage:
    def __init__(self):
        self._pages = {}

    def __uuid(self):
        return str(uuid.uuid4())

    # UUID -> Boolean
    def contains(self, page_id):
        return page_id in self._pages

    # HTML -> UUID
    def save_page(self, page_content):
        page_id = self.__uuid()
        self._pages[page_id] = page_content
        return page_id

    # UUID -> HTML
    def get_page(self, page_id):
        return self._pages.get(page_id)

    # UUID ->
    def remove_page(self, page_id):
        self._pages.pop(page_id)
