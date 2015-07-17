#!/usr/bin/env python3

import uuid

from bottle import template


class PageGenerator:
    def __init__(self):
        self._pages = {}
    
    def generate_page(self, client_url, media_type):
        id = self.__uuid()
        if media_type == 'image':
            template_src = 'simple_image_page'
        elif media_type == 'video':
            template_src = 'simple_video_page'
            
        page_content = template(template_src, media_url=client_url)
        self._pages[id] = page_content
        
        return id
    
    def __uuid(self):
        return str(uuid.uuid4())
        
    def retrieve_page(self, page_id):
        return self._pages.get(page_id)

    def has_generated(self, id):
        return id in self._pages
