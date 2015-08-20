import unittest

from remote_helper import filters


class DefaultFilterTest(unittest.TestCase):
    def setUp(self):
        self.filter = filters.DefaultFilter()

    def test_filter_should_block_a_matching_event(self):
        filtered_event = {
            'type': 'keydown',
            'content': {
                'code': 87,
                'modifiers': ['ctrlKey']
            }
        }
        self.assertEqual(self.filter.blocks(filtered_event), True)

    def test_filter_should_not_block_a_non_matching_event(self):
        non_filtered_event = {
            'type': 'mousedown',
            'content': {
                'button': 'left',
                'coordinates': {
                    'x': 140.2,
                    'y': 90.0
                }
            }
        }
        self.assertEqual(self.filter.blocks(non_filtered_event), False)

    def test_invalid_event_should_not_be_blocked(self):
        invalid_event = {
            'type': 'bogus',
            'content': {
                'code': 'n',
                'modifiers': ['foo', 'bar']
            }
        }
        self.assertEqual(self.filter.blocks(invalid_event), False)
