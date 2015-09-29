# -*- coding: utf-8 -*-
import logging
from functools import wraps

from ojos.misc.exceptions import ResponseException


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
            except ResponseException, e:
                if e.url is not None:
                    return _self.redirect(e.url, e.code)

                if e.code is None:
                    e.code = code

                if e.message is None:
                    e.message = message

                if e.header_code is None:
                    e.header_code = header_code

                return error(e, *args, **kwargs)
            except Exception, e:
                e.code = code
                e.message = message
                e.header_code = header_code
                return error(e, *args, **kwargs)
        return callf
    return decorator
