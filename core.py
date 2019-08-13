import argparse
import logging
from instagram.parser import InstaAccount
from mail.mailer import Mailer
from settings import USER_IDS
from store.storage import Storage


def check_media(args) -> None:
    mailer = Mailer()
    for user_id in args.usernames:
        account = InstaAccount(user_id)
        new_media = account.get_new_media()
        if new_media:
            mailer.send_mail_new_media_found(user_id, new_media)
        logging.info(f'{user_id} media were checked')


def check_stories(args) -> None:
    mailer = Mailer()
    for user_id in args.usernames:
        account = InstaAccount(user_id)
        if account.has_stories():
            mailer.send_mail_stories_found(user_id)
        logging.info(f'{user_id} stories were checked')


def init_storage(args) -> None:
    storage = Storage()
    storage.set_users_counter(args.usernames)


parser = argparse.ArgumentParser(description='Get email notification about instagram new posts and stories')
subparsers = parser.add_subparsers(help='List of commands')

media_parser = subparsers.add_parser('media', help='Get email notification about new instagram posts by users')
media_parser.add_argument('-u', '--usernames', nargs='+', help='instagram usernames')
media_parser.set_defaults(func=check_media)

stories_parser = subparsers.add_parser('stories', help='Get email notification about new instagram stories by users')
stories_parser.add_argument('-u', '--usernames', nargs='+', help='instagram usernames')
stories_parser.set_defaults(func=check_stories)

storage_parser = subparsers.add_parser('init', help='Init storage by username: count posts')
storage_parser.add_argument('-u', '--usernames', nargs='+', help='instagram usernames')
storage_parser.set_defaults(func=init_storage)

logging.basicConfig(level=logging.INFO)
args = parser.parse_args()
if not args.usernames:
    args.usernames = USER_IDS
args.func(args)

