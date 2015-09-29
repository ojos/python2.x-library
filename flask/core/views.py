# -*- coding: utf-8 -*-
from flask import (request, redirect)
from flask.views import MethodView

from werkzeug.http import HTTP_STATUS_CODES

from ojos.misc.decorators import error_response
from ojos.misc.utils import lazy_loader

try:
    import ujson as json
except:
    from flask import json

try:
    from flask.globals import current_app
    response_class = current_app.response_class
except:
    from flask.wrappers import Response
    response_class = Response


class BaseView(MethodView):
    _response = None

    @property
    def response(self):
        if self._response is None:
            self._response = response_class()

        return self._response

    def redirect(self, url, code=302):
        redirect(url, code=302)

    @error_response(code=405)
    def dispatch_request(self, *args, **kwargs):
        return super(BaseView, self).dispatch_request(*args, **kwargs)

    def status_message(self, code=500, *args, **kwargs):
        return HTTP_STATUS_CODES[code]

    def success(self, context, code=200, *args, **kwargs):
        res = self.response
        res.status_code = code
        res.set_data(self.success_context(context, *args, **kwargs))
        return res

    def success_context(self, context, *args, **kwargs):
        return context

    def error(self, message=None, code=500, header_code=True, *args, **kwargs):
        res = self.response
        if header_code:
            res.status_code = code
        res.set_data(self.error_context(message, code, *args, **kwargs))
        return res

    def error_context(self, message=None, code=500, *args, **kwargs):
        if message is None:
            msg = self.status_message(code)
            try:
                if msg == 'I\'m a teapot':
                    cls_name = 'ImATeapot'
                else:
                    cls_name = ''.join(msg.split(' '))

                error_cls = lazy_loader('werkzeug.exceptions.%s' % cls_name)
                return error_cls().get_body()
            except:
                return '%d %s' % (code, msg.upper())
        else:
            return message


class DownloadView(BaseView):
    def success(self, filename, context, code=200):
        res = self.response
        res.headers['Content-Type'] = 'application/octet-stream'
        res.headers['Content-Disposition'] =\
            'attachment; filename="%s"' % filename.encode('utf8')
        return super(DownloadView, self).success(context, code)


class ApiView(BaseView):
    @property
    def response(self):
        if self._response is None:
            self._response = response_class()
            self._response.headers['Access-Control-Allow-Origin'] = '*'
            self._response.headers['Access-Control-Allow-Headers'] = '*'
            self._response.headers['Access-Control-Allow-Methods'] =\
                'PUT,DELETE,POST,GET,OPTIONS'

        return self._response


class JsonView(BaseView):
    def json_context(self, context):
        res = self.response
        callback = request.args.get('callback', default=None)

        if callback is None:
            res.headers['Content-Type'] = 'application/json; charset=utf-8'
        else:
            res.headers['Content-Type'] = 'application/javascript; charset=utf-8'
            context = u'%s(%s);' % (callback, context)

        return context

    def success(self, code=200, *args, **kwargs):
        res = self.response
        res.status_code = code
        res.set_data(self.json_context(self.success_context(code, *args, **kwargs)))
        return res

    def success_context(self, code=200, *args, **kwargs):
        parent = {'code': code,
                  'message': self.status_message(code).upper()}
        context = dict(*args, **kwargs)
        if len(context) > 0:
            parent['content'] = context

        return json.dumps(parent)

    def error(self, message=None, code=500, header_code=True, *args, **kwargs):
        res = self.response
        if header_code:
            res.status_code = code
        res.set_data(self.json_context(self.error_context(message, code, *args, **kwargs)))
        return res

    def error_context(self, message=None, code=500, *args, **kwargs):
        if message is None:
            msg = self.status_message(code)
            parent = {'code': code,
                      'message': msg}
        else:
            parent = {'code': code,
                      'message': message}

        return json.dumps(parent)
