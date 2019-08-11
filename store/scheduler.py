from redis import Redis
from rq_scheduler import Scheduler
from core import check_media, check_stories
from settings import USER_IDS


scheduler = Scheduler(connection=Redis())

scheduler.cron(
    '0 */8 * * *',             # each 8 hours
    func=check_media,
    args=[USER_IDS],
)

scheduler.cron(
    '0 8 * * *',               # every day at 08:00 am
    func=check_stories,
    args=[USER_IDS],
)