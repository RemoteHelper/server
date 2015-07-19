#!/usr/bin/env python3

import uuid
import os.path

from bottle import template


class PageGenerator:
    def __init__(self):
        self._pages = {}
        self.base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

    # -> UUID
    def __uuid(self):
        return str(uuid.uuid4())

    # URL -> String -> UUID
    def generate_page(self, client_url, media_type):
        page_id = self.__uuid()

        if media_type == 'image':
            tpl_file = os.path.join(self.base_path, 'templates/simple_image_page')
        else:
            tpl_file = os.path.join(self.base_path, 'templates/simple_video_page')

        page_content = template(tpl_file, media_url=client_url)
        self._pages[page_id] = page_content
        
        return page_id

    # UUID -> HTML
    def retrieve_page(self, page_id):
        return self._pages.get(page_id)

    # UUID -> Boolean
    def has_generated(self, page_id):
        return page_id in self._pages

    # UUID ->
    def remove_page(self, page_id):
        self._pages.pop(page_id)
