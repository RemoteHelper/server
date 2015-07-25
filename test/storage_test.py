import unittest

from server import storage


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.storage = storage.Storage()

    def test_storage_should_return_false_on_non_existing_keys(self):
        self.assertEqual(self.storage.contains('made_up_key'), False)

    def test_storage_should_return_true_on_existing_keys(self):
        key = self.storage.save_page('content')
        self.assertEqual(self.storage.contains(key), True)

    def test_storage_should_return_original_content(self):
        key = self.storage.save_page('content')
        self.assertEqual(self.storage.get_page(key), 'content')

    def test_storage_should_delete_given_key(self):
        key = self.storage.save_page('content')
        self.storage.remove_page(key)
        self.assertEqual(self.storage.contains(key), False)

    def test_storage_should_raise_key_error_on_non_existing_key_deletion(self):
        self.assertRaises(Exception, self.storage.remove_page, 'bogus_key')


if __name__ == '__main__':
    unittest.main()
