import requests
from json import JSONDecodeError
from functools import lru_cache



class InstaAccount:
    def __init__(self, user_id: str):
        url = f"https://instagram.com/{user_id}/?__a=1"
        self.user_id = user_id
        response = requests.get(url, headers=InstaAgent().headers)
        try:
            self.data = response.json()['graphql']['user']['edge_owner_to_timeline_media']
        except JSONDecodeError:
            raise ValueError('Please check user_id. Only public accounts processed')

    def get_media_count(self) -> int:
        return int(self.data['count'])

    def get_media_description(self, num: int) -> str:
        try:
            return self.data['edges'][num]['node']['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            raise ValueError(f'Please check does {num} posts exist. Only public accounts processed')

    def get_media_link(self, num: int) -> str:
        try:
            return self.data['edges'][num]['node']['display_url']
        except IndexError:
            raise ValueError(f'Please check does {num} posts exist. Only public accounts processed')

    def get_new_media(self) -> list:
        from store.storage import Storage

        storage = Storage()
        old_media_count = storage.get_user_media_count(self.user_id)
        insta_info = InstaAccount(self.user_id)
        new_media_count = insta_info.get_media_count()
        storage.set_user_media_count(self.user_id, new_media_count)
        return [{'link': insta_info.get_media_link(i), 'description': insta_info.get_media_description(i)}
                for i in range(new_media_count - old_media_count)]

    def has_stories(self) -> bool:
        url = f"https://www.instagram.com/stories/{self.user_id}/?__a=1"
        response = requests.get(url, headers=InstaAgent().headers)
        try:
            response.json()
        except JSONDecodeError:
            return False
        return True


class InstaAgent:
    @property
    @lru_cache()
    def headers(self) -> dict:
        manufacturer = 'Xiaomi'
        model = 'HM 1SW'
        android_version = 18
        android_release = '4.3'
        user_agent = f'Instagram 10.26.0 Android ({android_version}/{android_release}; ' \
                     f'320dpi; 720x1280;{manufacturer}; {model}; armani; qcom; en_US)'

        return {'User-Agent': user_agent}
