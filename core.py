import logging
from instagram.parser import InstaAccount
from mail.mailer import Mailer
from settings import USER_IDS
from store.storage import Storage


def check_media(user_ids: list) -> None:
    mailer = Mailer()
    for user_id in user_ids:
        account = InstaAccount(user_id)
        new_media = account.get_new_media()
        if new_media:
            mailer.send_mail_new_media_found(user_id, new_media)
        logging.info(f'{user_id} media were checked')


def check_stories(user_ids: list) -> None:
    mailer = Mailer()
    for user_id in user_ids:
        account = InstaAccount(user_id)
        if account.has_stories():
            mailer.send_mail_stories_found(user_id)
        logging.info(f'{user_id} stories were checked')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    storage = Storage()
    storage.set_users_counter(USER_IDS)
    check_stories(USER_IDS)
    check_media(USER_IDS)
