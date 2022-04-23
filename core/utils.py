import datetime
import pytz
from config import get_settings


def now():
    settings = get_settings()
    return datetime.datetime.now(pytz.timezone(settings.TIMEZONE))