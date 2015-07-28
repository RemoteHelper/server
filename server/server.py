#!/usr/bin/env python3

import json

import requests
from bottle import run, abort, post, get, request, HTTPResponse, static_file, response

import job
import config
import filters
import storage
import page_generator

current_job = None


@get('/static/<filename:re:.*\.css>')
def get_css(filename):
    return static_file(filename, root='./static')


@get('/js/<filename:re:.*\.js>')
def get_js(filename):
    return static_file(filename, root='./js')


@post('/events')
def receive_events():
    """
    Process events coming from the user page

    receive_events :: {} -> Natural | {}

    Filters them according to the default filter set, and then forwards
    them to the client

    Returns: 100 | 200
    Payload: {}?
    """
    event = request.json

    if not event or current_job is None:
        return HTTPResponse(status=400)

    if event_filter.blocks(event):
        return HTTPResponse(status=100)

    events_url = current_job.get_events_url()
    if events_url is None or not _valid_event(event):
        return HTTPResponse(status=400)

    client_response = forward(events_url, event)

    return client_response if client_response else HTTPResponse(status=100)


def _valid_event(event):
    """
    Specifies if a given event is valid according to the spec

    _valid_event :: {} -> Bool

    Event should be exactly {'media': {'type': Any, 'content': [Any]}}
    """
    return {'media'} == set(event.keys()) and \
        isinstance(event['media'], dict) and \
        {'content', 'type'} == set(event['media'].keys()) and \
        isinstance(event['media']['content'], list)


def forward(destination, event):
    """
    Forwards the given event to the client

    forward :: {} -> {}?

    The client can then reply with 100 Continue, in which case we return None,
    or 200 and a media payload, in which case we return the media payload

    If the payload is wrong, return None
    """

    payload = event
    r = requests.post(destination, data=json.dumps(payload))

    status = r.status_code

    if status == 100:
        return None

    # else the status is 200
    result = r.json()
    if not result:
        return None

    return result if _valid_event(result) else None


@get('/api/stream')
def stream():
    """
    Server-Sent Events endpoint for the server

    Notifies the browser that we're done and that it should stop forwarding
    events.

    It should also notify the user of the next step
    (e.g. close the tab)
    """

    response.content_type = 'text/event-stream'
    response.cache_control = 'no-cache'

    # make the user page reconnect in 5s whenever the connection closes
    yield 'retry: 5000\n'

    if current_job is not None and current_job.is_complete():
        # send the browser the 'jobcomplete' message
        # the browser should then notify the user of this
        yield 'event: jobcomplete\n' + \
              'data: {"done":true}\n\n'


@post('/api/help/image')
def process_help():
    global current_job

    result = request.json

    media_type = 'image'
    media_url = result['media']['content']

    events_url = result['eventsURL']
    current_job = job.Job(events_url)

    page_content = page_generator.generate_page(media_url, media_type)
    page_id = storage.save_page(page_content)

    user_url = config.get_user_endpoint() + page_id
    done_url = config.get_done_url()

    return {
        "userURL": user_url,
        "doneURL": done_url
    }


@get('/resolve/<page_id>')
def serve_static_page(page_id):
    if not storage.contains(page_id):
        abort(404, 'Not found')

    return storage.get_page(page_id)


@post('/api/done')
def stop_help():
    """
    Stop forwarding events to the client.

    Receives the user url that the client was to unsubscribe from,
    if the url does not matches one we provided, respond with an 403
    error code, else return OK
    """

    if not request.json or current_job is None:
        return HTTPResponse(status=400)

    user_url = request.json['authURL']
    if user_url.endswith('/'):
        user_url = user_url[:-1]

    page_id = user_url.split('/')[-1]

    if not storage.contains(page_id):
        return HTTPResponse(status=403, body="Auth URL doesn't match!")

    current_job.complete_job()
    storage.remove_page(page_id)

    return HTTPResponse(status=200)


if __name__ == "__main__":
    storage = storage.Storage()
    event_filter = filters.DefaultFilter()

    run(host=config.get_domain_name(), port=config.get_domain_port(), debug=True)
