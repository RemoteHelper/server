#!/usr/bin/env python3

import uuid

from bottle import template


class PageGenerator:
    def __init__(self):
        self._pages = {}

    # -> UUID
    def __uuid(self):
        return str(uuid.uuid4())

    # URL -> String -> UUID
    def generate_page(self, client_url, media_type):
        page_id = self.__uuid()

        if media_type == 'image':
            template_src = 'simple_image_page'
        else:
            template_src = 'simple_video_page'
            
        page_content = template(template_src, media_url=client_url)
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
