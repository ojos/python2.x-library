# -*- coding: utf-8 -*-
import json

from django import http
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from ojos.misc.decorators import error_response
from ojos.misc.exceptions import MethodNotAllowedException


class BaseView(View):
    _response = None

    @property
    def response(self):
        if self._response is None:
            self._response = http.HttpResponse()

        return self._response

    def redirect(self, url, code=302):
        redirect = http.HttpResponseRedirect(url)
        redirect.status_code = code
        return redirect

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseView, self).dispatch(request, *args, **kwargs)

    def status_message(self, code=500):
        return http.response.REASON_PHRASES[code]

    def success(self, context, code=200, *args, **kwargs):
        res = self.response
        res.status_code = code
        res.content = self.success_context(context, *args, **kwargs)
        return res

    def success_context(self, context, *args, **kwargs):
        return context

    def error(self, message=None, code=500, header_code=True, *args, **kwargs):
        res = self.response
        if header_code:
            res.status_code = code
            res.reason_phrase = message
        res.content = self.error_context(message, code, *args, **kwargs)
        return res

    def error_context(self, message=None, code=500, *args, **kwargs):
        if message is None:
            return '%d %s' % (code, self.status_message(code))
        else:
            return message

    @error_response()
    def get(self, request, *args, **kwargs):
        raise MethodNotAllowedException()

    @error_response()
    def post(self, request, *args, **kwargs):
        raise MethodNotAllowedException()

    @error_response()
    def head(self, request, *args, **kwargs):
        raise MethodNotAllowedException()

    @error_response()
    def options(self, request, *args, **kwargs):
        raise MethodNotAllowedException()

    @error_response()
    def put(self, request, *args, **kwargs):
        raise MethodNotAllowedException()

    @error_response()
    def delete(self, request, *args, **kwargs):
        raise MethodNotAllowedException()

    @error_response()
    def trace(self, request, *args, **kwargs):
        raise MethodNotAllowedException()


class DownloadView(BaseView):

    def success(self, filename, context, code=200):
        res = self.response
        res['Content-Type'] = 'application/octet-stream'
        res['Content-Disposition'] =\
            'attachment; filename="%s"' % filename.encode('utf8')
        return super(DownloadView, self).success(context, code)


class ApiView(BaseView):

    @property
    def response(self):
        if self._response is None:
            self._response = http.HttpResponse()
            self._response['Access-Control-Allow-Origin'] = '*'
            self._response['Access-Control-Allow-Headers'] =\
                'Origin, Authorization, Accept, Content-Type'
            self._response['Access-Control-Allow-Methods'] =\
                'PUT,DELETE,POST,GET,OPTIONS'

        return self._response


class JsonView(BaseView):

    def json_context(self, context):
        res = self.response
        res['Content-Type'] = 'application/json; charset=utf-8'
        return context

    def success(self, code=200, *args, **kwargs):
        res = self.response
        res.status_code = code
        res.content = self.json_context(self.success_context(code, *args, **kwargs))
        return res

    def success_context(self, code=200, *args, **kwargs):
        parent = {'code': code,
                  'message': self.status_message(code).upper()}
        context = dict(*args, **kwargs)
        if len(context) > 0:
            parent['content'] = context

        return json.dumps(parent,
                          ensure_ascii=False,
                          encoding='utf8').strip()

    def error(self, message=None, code=500, header_code=True, *args, **kwargs):
        res = self.response
        if header_code:
            res.status_code = code
            res.reason_phrase = message
        res.content = self.json_context(self.error_context(message, code, *args, **kwargs))
        return res

    def error_context(self, message=None, code=500, *args, **kwargs):
        if message is None:
            msg = self.status_message(code)
            parent = {'code': code,
                      'message': msg}
        else:
            parent = {'code': code,
                      'message': message}

        return json.dumps(parent,
                          ensure_ascii=False,
                          encoding='utf8').strip()
