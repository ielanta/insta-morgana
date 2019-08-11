import unittest

from instagram.parser import InstaAccount


class InstagramTests(unittest.TestCase):
    def setUp(self):
        self.data = InstaAccount('instagram')

    def test_instagram_post_counter(self):
        count_posts = self.data.get_media_count()
        self.assertIsInstance(count_posts, int)
        self.assertGreater(count_posts, 5972)

    def test_instagram_media_description(self):
        description = self.data.get_media_description(0)
        self.assertIsInstance(description, str)
        self.assertTrue('Photo' in description or 'Video' in description)
        
    def test_instagram_media_link(self):
        link = self.data.get_media_link(0)
        self.assertIsInstance(link, str)
        self.assertIn('http', link)

    def test_instagram_has_stories(self):
        link = self.data.has_stories()
        self.assertIsInstance(link, bool)

    def test_not_existing_account(self):
        with self.assertRaises(ValueError) as context:
            InstaAccount('instagramfmjfdmjfdmdfjmjdfmjfdmjfd')
        self.assertEqual('Please check user_id. Only public accounts processed', str(context.exception))

    def test_private_account(self):
        data = InstaAccount('epicfunnypage')
        with self.assertRaises(ValueError) as context:
            data.get_media_link(0)
        self.assertEqual('Please check does 0 posts exist. Only public accounts processed', str(context.exception))
        with self.assertRaises(ValueError) as context:
            data.get_media_description(0)
        self.assertEqual('Please check does 0 posts exist. Only public accounts processed', str(context.exception))



if __name__ == "__main__":
    unittest.main()
