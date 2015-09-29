# -*- coding: utf-8 -*-
import base64
import logging

from functools import wraps


def basicauth(user_dict, realm):
    def decorator(f):
        @wraps(f)
        def callf(_self, *args, **kwargs):
            def _send_401(_self, message):
                _self.response.status_code = 401
                _self.response['WWW-Authenticate'] = 'Basic realm="%s"' % (realm)
                _self.response.content = '<body><h1>%s</h1></body>\n' % message
                return _self.response

            if 'HTTP_AUTHORIZATION' in _self.request.META:
                auth_header = _self.request.META['HTTP_AUTHORIZATION']
            elif 'Authorization' in _self.request.META:
                auth_header = _self.request.META['Authorization']
            else:
                auth_header = False
            msg = 'Basic authentication required'

            if auth_header:
                try:
                    (scheme, base64Str) = auth_header.split(' ')
                    if scheme == 'Basic':
                        (username, password) = base64.b64decode(base64Str).split(':')
                        if user_dict[username] == password:
                            _self.request.basic_user = username
                            return f(_self, *args, **kwargs)
                        else:
                            logging.info("failed login attempt :" + username)
                    else:
                        logging.error(
                            "got invalid scheme from client " + scheme)
                        msg = "Only the basic authentication is accepted."
                except KeyError, err:
                    logging.info("failed login attempt :" + username)
                except (ValueError, TypeError), err:
                    logging.info("failed to authenticate: " + err.__str__())
            return _send_401(_self, msg)
        return callf
    return decorator
