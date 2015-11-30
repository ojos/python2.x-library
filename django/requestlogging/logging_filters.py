# -*- coding: utf-8 -*-
from django_requestlogging.logging_filters import RequestFilter as _RequestFilter


class RequestFilter(_RequestFilter):

    def filter(self, record):
        request = self.request
        META = getattr(request, 'META', {})
        forwarded_for = META.get('HTTP_X_FORWARDED_FOR', '-').split(',')
        record.real_ip = http_x_forwarded_for[0].strip()
        return super(RequestFilter, self).filter(record)
