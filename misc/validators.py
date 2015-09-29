# -*- coding: utf-8 -*-
import base64
import json
import datetime
import math
import re
import time
from Crypto.Cipher import AES
from email.utils import parsedate

from .utils import (lazy_loader, time_to_i)


class Validator(object):
    def __init__(self, validate, default=None, exception=Exception, kwargs={}):
        self._validate = validate
        self._default = default
        self._exception = exception
        self._kwargs = kwargs

    @classmethod
    def get(cls, validate, default=None, exception=Exception, kwargs={}):
        _self = cls(validate, default, exception, kwargs)

        return _self

    def validate(self, value, default=None, exception=None, **kwargs):
        if default is None:
            default = self._default

        if exception is None:
            exception = self._exception

        _kwargs = self._kwargs.copy()
        _kwargs.update(kwargs)

        return self._validate(value=value, default=default, exception=exception,
                              **_kwargs)


def is_empty(value, exception=Exception):
    if isinstance(value, list) or\
            isinstance(value, tuple) or\
            isinstance(value, dict):
        if len(value) == 0:
            raise exception
    else:
        if exception is not None and\
                (value is None or value.isspace() or value == ''):
            raise exception

    return value


def is_digits(value, digits, operator='!=', exception=Exception):
    n = int(math.log10(value) + 1)
    if exception is not None and\
            ((operator == '==' and n != digits) or
             (operator == '!=' and n == digits) or
             (operator == '<' and n >= digits) or
             (operator == '>' and n <= digits) or
             (operator == '<=' and n > digits) or
             (operator == '>=' and n < digits)):
        raise exception

    return value


def encrypt_aes(value, key, limit=32, fill_str='*', ascii=True,
                default=None, exception=Exception):
    try:
        if value is None:
            raise

        msg = validate_str(value).ljust(limit, fill_str)
        cipher = AES.new(key)
        data = cipher.encrypt(msg)
        if ascii:
            data = base64.urlsafe_b64encode(data)

        return data
    except:
        if exception is not None and default is None:
            raise exception
        else:
            return validate_value(default)


def decrypt_aes(value, key, fill_str='*', ascii=True,
                default=None, exception=Exception):
    try:
        if value is None:
            raise

        cipher = AES.new(key)
        if ascii:
            value = base64.urlsafe_b64decode(validate_str(value))
        msg = cipher.decrypt(value)

        return msg[0:msg.find(fill_str)]
    except:
        if exception is not None and default is None:
            raise exception
        else:
            return validate_value(default)


def no_validate(value, default=None, exception=Exception):
    if value is None:
        value = default
    return value


def validate_value(value):
    try:
        return eval(value)
    except:
        return value


def validate_str(value, default=None, exception=Exception):
    try:
        if value is None:
            value = validate_value(default)
        return str(value)
    except:
        if exception is not None and default is None:
            raise exception
        else:
            return validate_value(default)


def validate_unicode(value, default=None, exception=Exception):
    try:
        if value is None:
            value = validate_value(default)
        return unicode(value)
    except:
        if exception is not None and default is None:
            raise exception
        else:
            return validate_value(default)


def validate_int(value, default=None, exception=Exception):
    try:
        if isinstance(value, datetime.datetime) or\
                isinstance(value, datetime.date):
            _value = time_to_i(value)
        else:
            _value = int(value)
    except:
        if exception is not None and default is None:
            raise exception
        else:
            return validate_value(default)

    return _value


def validate_float(value, default=None, exception=Exception):
    try:
        _value = float(value)
    except:
        if exception is not None and default is None:
            raise exception
        else:
            return validate_value(default)

    return _value


def validate_bool(value, default=None, exception=Exception):
    if isinstance(value, bool):
        return value
    elif isinstance(value, str) or isinstance(value, unicode):
        if value.isdigit():
            return bool(int(value))
        else:
            return value == 'true'
    elif isinstance(value, list) or\
            isinstance(value, tuple) or\
            isinstance(value, dict):
        return len(value) > 0

    try:
        return validate_int(value, exception) > 0
    except:
        if exception is not None and default is None:
            raise exception
        else:
            return validate_value(default)


def validate_datetime(value, default=None, exception=Exception):
    if isinstance(value, datetime.datetime):
        return value
    elif isinstance(value, datetime.date):
        return datetime.datetime.combine(value, datetime.time())
    elif isinstance(value, list) or isinstance(value, tuple):
        try:
            return datetime.datetime(*[validate_int(v) for v in value])
        except:
            pass
    elif isinstance(value, dict):
        try:
            return datetime.datetime(*[validate_int(v) for v in value.values()])
        except:
            pass
    else:
        if isinstance(value, str) or isinstance(value, unicode):
            try:
                return datetime.datetime(*(parsedate(value)[:6]))
            except:
                pass

        try:
            return datetime.datetime.fromtimestamp(validate_int(value))
        except:
            pass

    if exception is not None and default is None:
        raise exception
    else:
        return validate_value(default)


def validate_date(value, default=None, exception=Exception):
    if isinstance(value, datetime.date):
        return value
    elif isinstance(value, datetime.datetime):
        return value.date()
    elif isinstance(value, list) or isinstance(value, tuple):
        try:
            return datetime.date(*[validate_int(v) for v in value])
        except:
            pass
    elif isinstance(value, dict):
        try:
            return datetime.date(*[validate_int(v) for v in value.values()])
        except:
            pass
    else:
        try:
            return datetime.datetime.fromtimestamp(validate_int(value)).date()
        except:
            pass

    if exception is not None and default is None:
        raise exception
    else:
        return validate_value(default)


def validate_time(value, default=None, exception=Exception):
    if isinstance(value, time):
        return value
    elif isinstance(value, datetime.datetime):
        return value.time()
    elif isinstance(value, list) or isinstance(value, tuple):
        try:
            return datetime.date(*[validate_int(v) for v in value])
        except:
            pass
    elif isinstance(value, dict):
        try:
            return datetime.date(*[validate_int(v) for v in value.values()])
        except:
            pass
    else:
        value = validate_int(value)
        try:
            s = value % 60
            m = value / 60
            h = m / 60
            m = m % 60
            return datetime.time(h, m, s)
        except:
            pass

    if exception is not None and default is None:
        raise exception
    else:
        return validate_value(default)


def validate_timedelta(value, default=None, exception=Exception):
    if isinstance(value, datetime.timedelta):
        return value
    elif isinstance(value, list) or isinstance(value, tuple):
        try:
            return datetime.timedelta(**dict(zip(['hours', 'minutes', 'seconds'],
                                                 [validate_int(v) for v in value])))
        except:
            pass
    elif isinstance(value, dict):
        try:
            return datetime.timedelta(**value)
        except:
            pass
    else:
        try:
            return datetime.timedelta(validate_int(value))
        except:
            pass

    if exception is not None and default is None:
        raise exception
    else:
        return validate_value(default)


def validate_list(value, default=None, exception=Exception, sep=',', reg=False,
                  sub_validate=None, sub_default=None, sub_exception=Exception):
    try:
        if isinstance(value, list):
            _value = value
        elif isinstance(value, str) or isinstance(value, unicode):
            if reg:
                _value = re.split(sep, value)
            else:
                _value = value.split(sep)
        elif isinstance(value, dict):
            _value = value.items()
        elif isinstance(value, int) or isinstance(value, float) or\
                isinstance(value, long) or isinstance(value, complex):
            _value = [value]
        else:
            _value = list(value)
    except:
        if exception is not None and default is None:
            raise exception
        else:
            return validate_value(default)

    if sub_validate is None:
        return _value
    else:
        if hasattr(sub_validate, 'validate'):
            _sub_validate = sub_validate.validate
        else:
            _sub_validate = sub_validate

        return [_sub_validate(i, default=sub_default,
                              exception=sub_exception) for i in _value]


def validate_list_in_bool(value, default=None, exception=Exception,
                          sep=',', reg=False, sub_default=None,
                          sub_exception=Exception):
    return validate_list(value, default, exception, sep, reg,
                         validate_bool, sub_default, sub_exception)


def validate_list_in_int(value, default=None, exception=Exception,
                         sep=',', reg=False, sub_default=None,
                         sub_exception=Exception):
    return validate_list(value, default, exception, sep, reg,
                         validate_int, sub_default, sub_exception)


def validate_list_in_str(value, default=None, exception=Exception,
                         sep=',', reg=False, sub_default=None,
                         sub_exception=Exception):
    return validate_list(value, default, exception, sep, reg,
                         validate_str, sub_default, sub_exception)


def validate_dict(value, default=None, exception=Exception,
                  sub_validate=None, sub_default=None, sub_exception=Exception):
    try:
        if isinstance(value, dict):
            value = value
        elif isinstance(value, str) or isinstance(value, unicode):
            value = json.loads(value)
        else:
            value = dict(value)
    except:
        if exception is not None and default is None:
            raise exception
        else:
            return validate_value(default)

    if sub_validate is None:
        return value
    else:
        if hasattr(sub_validate, 'validate'):
            _sub_validate = sub_validate.validate
        else:
            _sub_validate = sub_validate

        _value = {}
        for k, v in value.items():
            _value[k] = _sub_validate(v, default=sub_default,
                                      exception=sub_exception)
        return _value


def validate_range(value, default=None, exception=Exception, sep=',', reg=False,
                   sub_validate=validate_int, sub_default=None,
                   sub_exception=Exception):
    value = validate_list(value, default, exception, sep, reg,
                          sub_validate, sub_default, sub_exception)

    try:
        value = [min(value), max(value)]
    except:
        if exception is not None:
            raise exception

    return value


def validate_module(value, default=None, exception=Exception):
    try:
        lazy_loader(value)
    except:
        if exception is not None and default is None:
            raise exception
        else:
            return validate_value(default)

    return value


def validate_json(value, default=None, exception=Exception):
    try:
        json.loads(value)
        _value = value
        return _value
    except:
        try:
            if value is not None:
                _value = json.dumps(value)
                return _value
        except:
            pass

    if exception is not None and default is None:
        raise exception
    else:
        return validate_value(default)


def validate_csv(value, default=None, exception=Exception, sep=',', reg=False,
                 sub_default=None, sub_exception=Exception):
    if isinstance(value, str) or isinstance(value, unicode):
        return value
    else:
        try:
            value = validate_list_in_str(value, default, exception, sep, reg,
                                         sub_default, sub_exception)
            return ','.join(value)
        except:
            if exception is not None and default is None:
                raise exception
            else:
                return validate_value(default)


def validate_katakana(value, exception=Exception):
    """
    文字コード（utf-8）に依存しているコードです
    """
    if re.match(u'^[ぁ-ん]+$', value, re.U) is None:
        raise exception
    return value


def validate_hiragana(value, exception=Exception):
    """
    文字コード（utf-8）に依存しているコードです
    """
    if re.match(u'^[ァ-ン]+$', value, re.U) is None:
        raise exception
    return value


def validate_katakana_name(value, exception=Exception):
    if re.match(u'^[ァ-ン]+\s[ァ-ン]+$', value, re.U) is None:
        raise exception
    return value


def validate_hiragana_name(value, exception=Exception):
    if re.match(u'^[ぁ-ん]+\s[ぁ-ん]+$', value, re.U) is None:
        raise exception
    return value


def validate_mail(value, exception=Exception):
    if re.match(u'^[\w\-\+][\w\-\+\.]*@[\w\-][\w\-\.]+[a-zA-Z]{1,4}$',
                value, re.I) is None:
        raise exception
    return value


def validate_postcode(value, exception=Exception):
    if re.match(u'^\d{3}-\d{4}$', value) is None:
        raise exception
    return value


def validate_tel(value, exception=Exception):
    if re.match(u'^\d{2,4}-\d{2,4}-\d{4}$', value) is None:
        raise exception
    return value
