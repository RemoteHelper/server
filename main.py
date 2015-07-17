#!/usr/bin/env python3

import json

from bottle import run, abort, post, get, request, HTTPResponse

from page_generator import PageGenerator


page_generator = PageGenerator()
EVENTS_URL = None
STATIC_PAGES = {}
USER_URL = None

# -> {}
def load_config(config_file):
    with open(config_file, 'r') as config:
        return json.load(config)


# {} -> {}
@post('/api/help/image')
def process_help():
    global MEDIA_TYPE
    global EVENTS_URL
    global USER_URL

    media_url = request.json['media']['content']
    EVENTS_URL = request.json['eventsURL']
    
    id = page_generator.generate_page(media_url)
    USER_URL = host + '/resolve/' + page_generator.retrieve_page(id)
    return {"userURL": USER_URL, "doneURL": DONE_URL}


@get('/resolve/<an_uuid>')
def serve_static_page(an_uuid):
    if page_generator.has_generated(an_uuid):
        return page_generator.retrieve_page(an_uuid)

    abort(404, 'Not found')

# {} -> Response[status: Either<200|403> body?]
@post('/api/done')
def stop_help():
    return HTTPResponse(status=200) \
        if request.json and request.json['authURL'] == USER_URL \
        else HTTPResponse(status=403, body="Auth URL doesn't match!")


if __name__ == "__main__":
    config = load_config('config.json')
    host = config['host']['protocol'] + config['host']['url'] + ":" + str(config['host']['port'])
    DONE_URL = host + config['done_endpoint']
    run(host=config['host']['url'], port=config['host']['port'], debug=True)
