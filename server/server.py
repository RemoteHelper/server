#!/usr/bin/env python3

from bottle import run, abort, post, get, request, HTTPResponse

import page_generator
import config as configuration


@post('/api/help/image')
def process_help():
    result = request.json

    media_type = 'image'
    media_url = result['media']['content']

    page_id = page_generator.generate_page(media_url, media_type)
    user_url = config.get_user_endpoint() + page_id

    done_url = config.get_done_url()

    return {
        "userURL": user_url,
        "doneURL": done_url
    }


@get('/resolve/<page_id>')
def serve_static_page(page_id):
    if not page_generator.has_generated(page_id):
        abort(404, 'Not found')

    return page_generator.retrieve_page(page_id)


@post('/api/done')
def stop_help():
    """
    Stop forwarding events to the client.

    Receives the user url that the client was to unsubscribe from,
    if the url does not matches one we provided, respond with an 403
    error code, else return OK
    """

    if not request.json:
        return HTTPResponse(status=400)

    user_url = request.json['authURL']
    if user_url.endswith('/'):
        user_url = user_url[:-1]

    page_id = user_url.split('/')[-1]

    if not page_generator.has_generated(page_id):
        return HTTPResponse(status=403, body="Auth URL doesn't match!")

    page_generator.remove_page(page_id)
    return HTTPResponse(status=200)


if __name__ == "__main__":
    config = configuration.Config('config.json')
    page_generator = page_generator.PageGenerator()

    run(host=config.get_domain_name(), port=config.get_domain_port(), debug=True)
