#!/usr/bin/env python3

import requests
from bottle import run, abort, post, get, request, HTTPResponse, static_file, response

from job_container import JobContainer
import config
import filters
import storage
import page_generator
import schema_validator as sv

job = JobContainer()


@get('/static/<filename:re:.*\.css>')
def get_css(filename):
    return static_file(filename, root='./static')


@get('/js/<filename:re:.*\.js>')
def get_js(filename):
    return static_file(filename, root='./js')


@post('/api/help/image')
def process_help():
    request_data = request.json
    if not sv.valid_help_request(request_data) or job.is_running():
        return HTTPResponse(status=400)

    media_type = 'image'

    media_url = request_data['mediaURL']
    events_url = request_data['eventsURL']

    job.create_new(events_url)

    page_content = page_generator.generate_page(media_url, media_type)
    page_id = storage.save_page(page_content)

    return {
        "userURL": config.get_user_endpoint() + page_id,
        "doneURL": config.get_done_url()
    }


@get('/resolve/<page_id>')
def serve_static_page(page_id):
    if not storage.contains(page_id):
        abort(404, 'Not found')

    return storage.get_page(page_id)


@post('/events')
def receive_events():
    """
    Process events coming from the user page

    receive_events :: {} -> Natural | {}

    Filters them according to the default filter set, and then forwards
    them to the client

    If a payload is sent, the user should update old content with the payload

    Returns: 200
    Payload: {}?
    """

    event = request.json

    if not sv.valid_event(event) or job.is_complete():
        return HTTPResponse(status=400)

    if event_filter.blocks(event):
        return HTTPResponse(status=200)

    events_url = job.get_events_url()

    client_response = _forward(events_url, event)

    return client_response if client_response else HTTPResponse(status=200)


def _forward(destination, event):
    """
    Forwards the given event to the client

    forward :: {} -> {}?

    The client can then reply with an empty body, in which case we return None,
    or a media payload, in which case we return the media payload

    If the payload is wrong, return None
    """

    payload = event
    try:
        r = requests.post(destination, json=payload, timeout=10)
    except requests.Timeout as e:
        print('Timeout error: {}'.format(e))
        raise e

    status = r.status_code

    if status != 200:
        return None

    if not r.text or r.json() is None:
        return None

    client_response = r.json()
    return client_response if sv.valid_media(client_response) else None


@get(config.get_done_endpoint())
def get_done_status():
    """
    User done endpoint

    The browser will keep polling this function to know if
    it has to stop sending events.

    TODO:
    Should it also notify the user of the next step?
    """
    return {
        'done': job.is_complete()
    }


@post(config.get_done_endpoint())
def stop_help():
    """
    Stop forwarding events to the client.

    Receives the user url that the client was to unsubscribe from,
    if the url does not matches one we provided, respond with an 403
    error code, else return OK
    """

    request_data = request.json
    if not request_data or 'authURL' not in request_data or job.is_complete():
        return HTTPResponse(status=400)

    page_id = _get_page_id(request_data['authURL'])

    if not storage.contains(page_id):
        return HTTPResponse(status=403, body="Auth URL doesn't match!")

    job.complete()
    storage.remove_page(page_id)

    return HTTPResponse(status=200)


def _get_page_id(auth_url):
    return _remove_trailing_slash(auth_url).split('/')[-1]

def _remove_trailing_slash(url):
    return url[:-1] if url.endswith('/') else url



if __name__ == "__main__":
    storage = storage.Storage()
    event_filter = filters.DefaultFilter()

    run(host=config.get_domain_name(), port=config.get_domain_port(), debug=True)
