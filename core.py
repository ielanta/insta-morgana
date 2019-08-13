import argparse
import logging
import schedule
import time
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


def run_schedule(args):
    schedule.every(8).hours.do(check_media, args)
    schedule.every().day.at("08:00").do(check_stories, args)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get email notification about instagram new posts and stories')
    parser.add_argument('-u', '--usernames', nargs='+', help='instagram usernames', default=USER_IDS)
    subparsers = parser.add_subparsers(title='actions')

    media_parser = subparsers.add_parser('media', help='Get email notification about new instagram posts',
                                         parents=[parser], add_help=False)
    media_parser.set_defaults(func=check_media)

    stories_parser = subparsers.add_parser('stories', help='Get email notification about new instagram stories',
                                           parents=[parser], add_help=False)
    stories_parser.set_defaults(func=check_stories)

    storage_parser = subparsers.add_parser('init', help='Init storage by username: count posts',
                                           parents=[parser], add_help=False)
    storage_parser.set_defaults(func=init_storage)

    schedule_parser = subparsers.add_parser('schedule', help='Check new posts and stories by schedule',
                                            parents=[parser], add_help=False)
    schedule_parser.set_defaults(func=run_schedule)

    logging.basicConfig(level=logging.INFO)
    params = parser.parse_args()
    params.func(params)
