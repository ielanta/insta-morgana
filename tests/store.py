import unittest

from store.storage import Storage


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()
        self.user_id = 'instagram'

    def test_storage_set_value(self):
        value = 11
        self.storage.set_user_media_count(self.user_id, value)
        self.assertEqual(self.storage.get_user_media_count(self.user_id), value)

    def test_storage_get_value(self):
        value = 12
        self.storage.set_user_media_count(self.user_id, value)
        self.assertEqual(self.storage.get_user_media_count(self.user_id), value)
        self.assertEqual(int(self.storage._storage.get(self.user_id)), value)


if __name__ == "__main__":
    unittest.main()
