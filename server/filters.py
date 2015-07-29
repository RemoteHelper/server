#!/usr/bin/env python3


class DefaultFilter():
    def __init__(self):
        self._filter = [
            (87,    ('ctrlKey',)),              # ^W
            (87,    ('metaKey',)),              # ⌘W
            (87,    ('ctrlKey', 'shiftKey')),   # shift + ^W

            (81,    ('ctrlKey',)),              # ^Q
            (81,    ('metaKey',)),              # ⌘Q

            (115,   ('ctrlKey',)),              # ^F4
            (115,   ('altKey',))                # alt + F4
        ]

    # Event -> Bool
    def blocks(self, event):
        if event['type'] != 'keydown':
            return False

        key = tuple([event['content']['code'], tuple(event['content']['modifiers'])])
        return key in self._filter
