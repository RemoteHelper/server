#!/usr/bin/env python3

import json
import uuid

from bottle import run, abort, post, get, request, HTTPResponse, template

MEDIA = None
MEDIA_TYPE = None
EVENTS_URL = None
USER_URL = None

STATIC_PAGES = {}

# -> {}
def load_config(config_file):
    with open(config_file, 'r') as config:
        return json.load(config)

# {} -> {}
@post('/api/help/image')
def process_help():
    global MEDIA
    global MEDIA_TYPE
    global EVENTS_URL

    MEDIA = request.json['media']['content']
    MEDIA_TYPE = request.json['media']['type']
    EVENTS_URL = request.json['eventsURL']

    generate_static_page()

    return {"userURL": USER_URL, "doneURL": DONE_URL}

def generate_static_page():
    global USER_URL

    if MEDIA_TYPE == 'url':
        static_page_html = template('static_user_page_by_url', media_url=MEDIA)
        a_new_uuid = generate_page_uuid()
        STATIC_PAGES[a_new_uuid] = static_page_html
        USER_URL = host + config['user_endpoint'] + a_new_uuid

def generate_page_uuid():
    return str(uuid.uuid4())

@get('/resolve/<an_uuid>')
def serve_static_page(an_uuid):
    if an_uuid in STATIC_PAGES:
        return STATIC_PAGES[an_uuid]

    abort(404, 'Not found')


# {} -> Response[status: Either<200|403> body?]
@post('/api/done')
def stop_help():
    return HTTPResponse(status=200) \
        if request.json and request.json['authURL'] == USER_URL \
        else HTTPResponse(status=403, body="Auth url doesn't match!")

if __name__ == "__main__":
    config = load_config('config.json')
    host = config['host']['protocol'] + config['host']['url'] + ":" + str(config['host']['port'])
    DONE_URL = host + config['done_endpoint']
    run(host=config['host']['url'], port=config['host']['port'], debug=True)
