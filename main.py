#!/usr/bin/env python3

import json
from bottle import route, run, post, request, HTTPResponse

MEDIA = None
MEDIA_TYPE = None
EVENTS_URL = None

# -> {}
def load_config(config_file):
    with open(config_file, 'r') as config:
        return json.load(config)

# {} -> {}
@post('/api/help/image')
def process_help():
    MEDIA = request.json['media']['content']
    MEDIA_TYPE = request.json['media']['type']
    EVENTS_URL = request.json['eventsURL']
    return {"userURL": user_url, "doneURL": done_url}

# {} -> Response[status: Either<200|403> body?]
@post('/api/done')
def stop_help():
    return HTTPResponse(status=200) \
        if request.json and request.json['authURL'] == user_url \
        else HTTPResponse(status=403, body="Auth url doesn't match!")

if __name__ == "__main__":
    config = load_config('config.json')
    host = config['host']['protocol'] + config['host']['url'] + ":" + str(config['host']['port'])
    user_url = host + config['user_endpoint']
    done_url = host + config['done_endpoint']
    run(host=config['host']['url'], port=config['host']['port'], debug=True)
