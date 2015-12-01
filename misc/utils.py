# -*- coding: utf-8 -*-
import datetime
import random
import string
import time


def time_to_i(dt):
    try:
        return int(time.mktime(dt.timetuple()))
    except:
        return None


def time_from_i(i):
    try:
        return datetime.datetime.fromtimestamp(i)
    except:
        return None


def time_to_s(s):
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
    except:
        return None


def current_timestamp_int():
    return time_to_i(datetime.datetime.now())


def jst_date(value=None):
    if not value:
        value = datetime.datetime.now()
    utc = TimeZoneInfo.UtcTzinfo()
    jst = TimeZoneInfo.JstTzinfo()
    value = value.replace(tzinfo=utc).astimezone(jst)
    return value


def utc_date(value=None):
    utc = TimeZoneInfo.UtcTzinfo()
    if not value:
        value = datetime.datetime.now()
        value = value.replace(tzinfo=utc)
    else:
        value = value.astimezone(utc)
    return value


class TimeZoneInfo(object):

    class UtcTzinfo(datetime.tzinfo):

        def utcoffset(self, dt):
            return datetime.timedelta(0)

        def dst(self, dt):
            return datetime.timedelta(0)

        def tzname(self, dt):
            return 'UTC'

        def olsen_name(self):
            return 'UTC'

    class JstTzinfo(datetime.tzinfo):

        def utcoffset(self, dt):
            return datetime.timedelta(hours=9)

        def dst(self, dt):
            return datetime.timedelta(0)

        def tzname(self, dt):
            return 'JST'

        def olsen_name(self):
            return 'Asia/Tokyo'


def try_except(value, validate=lambda x: min(x), default=None):
    try:
        return validate(value)
    except:
        return default(value) if callable(default) else default


def uniq_str(len=8, add_str=''):
    return ''.join([random.choice(string.ascii_letters + string.digits + add_str)
                    for i in range(len)])


def set_trace():
    import pdb
    import sys
    debugger = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)
    debugger.set_trace(sys._getframe().f_back)


def lazy_loader(name):
    try:
        mod = __import__(name)
    except:
        mod_list = name.split('.')
        mod = __import__('.'.join(mod_list[:-1]))

    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


# def detect_imagetype(image):
#     if image[6:10] == 'JFIF':
#         return 'image/jpeg', 'jpeg'
#     if image[0:3] == 'GIF':
#         return 'image/gif', 'gif'
#     if image[1:4] == 'PNG':
#         return 'image/png', 'png'
