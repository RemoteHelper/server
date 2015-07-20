#!/usr/bin/env python3

import os.path

from bottle import template

base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')


# URL -> String -> HTML
def generate_page(client_url, media_type):
    if media_type == 'image':
        tpl_file = os.path.join(base_path, 'templates/simple_image_page')
    else:
        tpl_file = os.path.join(base_path, 'templates/simple_video_page')

    return template(tpl_file, media_url=client_url)
