import unittest

from bottle import template
from server import page_generator as generator

image_template_path = 'templates/simple_image_page'
video_template_path = 'templates/simple_video_page'


class PageGeneratorTest(unittest.TestCase):
    def test_generating_an_image_page_should_return_the_image_template_with_the_supplied_url(self):
        self.assertEqual(generator.generate_page('some_url', 'image'),
                         template(image_template_path, media_url='some_url'))

    def test_generating_a_video_page_should_return_the_image_template_with_the_supplied_url(self):
        self.assertEqual(generator.generate_page('some_url', 'video'),
                         template(video_template_path, media_url='some_url'))

    def test_generated_pages_should_default_to_video_if_unknown_media_type_is_given(self):
        self.assertEqual(generator.generate_page('some_url', '???'),
                         template(video_template_path, media_url='some_url'))


if __name__ == '__main__':
    unittest.main()
