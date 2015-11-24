# -*- coding: utf-8 -*-
import logging
import sys
from functools import wraps
from time import sleep

from ojos.misc.exceptions import ResponseException
from ojos.misc.scheduler import RepeatedTimer


# レスポンスエラーデコレータ
def error_response(code=500, message=None, header_code=True):
    def decorator(f):
        @wraps(f)
        def callf(_self, *args, **kwargs):
            def error(exception, *args, **kwargs):
                logging.exception(exception)
                return _self.error(e.message, e.code, e.header_code, *args, **kwargs)

            try:
                return f(_self, *args, **kwargs)
            except ResponseException as e:
                if e.url is not None:
                    return _self.redirect(e.url, e.code)

                if e.code is None:
                    e.code = code

                if e.message is None:
                    e.message = message

                if e.header_code is None:
                    e.header_code = header_code

                return error(e, *args, **kwargs)
            except Exception as e:
                e.code = code
                e.message = message
                e.header_code = header_code
                return error(e, *args, **kwargs)
        return callf
    return decorator


# リトライデコレータ
def retries(max_tries, delay=0, backoff=0, exceptions=(Exception,), hook=None):
    def decorator(f):
        @wraps(f)
        def callf(*args, **kwargs):
            mydelay = delay
            tries = range(max_tries)
            tries.reverse()
            for tries_remaining in tries:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    if tries_remaining > 0:
                        if hook is not None:
                            hook(tries_remaining, e, mydelay)
                        sleep(mydelay)
                        mydelay = mydelay * backoff
                    else:
                        raise
                else:
                    break
        return callf
    return decorator
