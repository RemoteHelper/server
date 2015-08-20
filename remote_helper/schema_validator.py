#!/usr/bin/env python3

import copy

from jsonschema import validate, ValidationError

_common_event_schema = {
    'type': 'object',
    'properties': {
        'type': {
            'type': 'string',
            'pattern': '^(mousedown|mouseup|keydown)$'
        },
        'timestamp': {
            'type': 'integer'
        }
    }
}

mouse_event_schema = copy.deepcopy(_common_event_schema)
mouse_event_schema['properties']['content'] = {
    'type': 'object',
    'properties': {
        'button': {
            'type': 'string',
            'pattern': '^(left|middle|right)$'
        },
        'coordinates': {
            'type': 'object',
            'properties': {
                'x': {
                    'type': 'number',
                    'minimum': 0.0
                },
                'y': {
                    'type': 'number',
                    'minimum': 0.0
                }
            },
            'required': ['x', 'y']
        }
    },
    'required': ['button', 'coordinates']
}
mouse_event_schema['required'] = ['type', 'content', 'timestamp']

keyboard_event_schema = copy.deepcopy(_common_event_schema)
keyboard_event_schema['properties']['content'] = {
    'type': 'object',
    'properties': {
        'code': {
            'type': 'integer'
        },
        'modifiers': {
            'type': 'array',
            'items': {
                'type': 'string',
                'pattern': '^(ctrlKey|altKey|shiftKey|metaKey)$'
            }
        }
    },
    'required': ['code', 'modifiers']
}

media_schema = {
    'type': 'object',
    'properties': {
        'mediaURL': {
            'type': 'string',
            'format': 'uri'
        }
    },
    'required': ['mediaURL']
}

help_schema = copy.deepcopy(media_schema)
help_schema['properties']['eventsURL'] = {
    'eventsURL': {
        'type': 'string',
        'format': 'uri'
    }
}
help_schema['required'] += ['eventsURL']


def valid_event(event):
    return _is_valid(event, keyboard_event_schema) or \
        _is_valid(event, mouse_event_schema)


def valid_media(payload):
    return _is_valid(payload, media_schema)


def valid_help_request(payload):
    return _is_valid(payload, help_schema)


def _is_valid(payload, schema):
    try:
        validate(payload, schema)
        return True
    except ValidationError:
        return False
