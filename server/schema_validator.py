#!/usr/bin/env python3

from jsonschema import validate, ValidationError

common_event_schema = {
    'type': {
        'type': 'string',
        'pattern': '^(mousedown|mouseup|keydown)$'
    },
    'timestamp': 'integer'
}

mouse_event_schema = dict(common_event_schema)
mouse_event_schema['content'] = {
    'button': {
        'type': 'string',
        'pattern': '^(left|middle|right)$'
    },
    'coordinates': {
        'x': {
            'type': 'number',
            'minimum': 0.0
        },
        'y': {
            'type': 'number',
            'minimum': 0.0
        }
    }
}

keyboard_event_schema = dict(common_event_schema)
keyboard_event_schema['content'] = {
    'code': 'integer',
    'modifiers': {
        'type': 'array',
        'items': {
            'type': {
                'type': 'string',
                'pattern': '^(ctrlKey|altKey|shiftKey|metaKey)$'
            }
        }
    }
}

media_schema = {
    'mediaURL': {
        'type': 'string',
        'pattern': 'uri'
    }
}

help_schema = dict(media_schema)
help_schema['eventsURL'] = {
    'eventsURL': {
        'type': 'string',
        'format': 'uri'
    }
}


def valid_event(event):
    return _validate(event, keyboard_event_schema) or \
        _validate(event, mouse_event_schema)


def valid_media(payload):
    return _validate(payload, media_schema)


def valid_help_request(payload):
    return _validate(payload, help_schema)


def _validate(payload, schema):
    try:
        validate(schema, payload)
        return True
    except ValidationError:
        return False
