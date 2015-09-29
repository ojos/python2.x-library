# -*- coding: utf-8 -*-
from ojos.flask.core.views import BaseView


class ProxyView(BaseView):
    client = None
    key = '/'

    def success(self, key=None, *args, **kwargs):
        res = self.response
        res.set_data(self.success_context(key))
        return res

    def success_context(self, key=None, *args, **kwargs):
        _key = self.key if key is None else key

        print self.client

        context = self.client.get(_key, cache=False)
        self.response.headers['Content-Type'] = self.client.get_content_type()
        return context
