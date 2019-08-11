from redis import Redis
from instagram.parser import InstaAgent, InstaAccount


class Storage:
    def __init__(self):
        self.agent = InstaAgent()
        self._storage = Redis(host='localhost', port=6379, db=0)

    def set_users_counter(self, user_ids: list):
        for user_id in user_ids:
            if not self._storage.get(user_id):
                media_count = InstaAccount(user_id).get_media_count()
                self.set_user_media_count(user_id, media_count)

    def get_user_media_count(self, user_id: str) -> int:
        return int(self._storage.get(user_id))

    def set_user_media_count(self, user_id: str, value: int):
        return self._storage.set(user_id, value)
