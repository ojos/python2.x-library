# -*- coding: utf-8 -*-
from django_requestlogging.logging_filters import RequestFilter as _RequestFilter


class RequestFilter(_RequestFilter):

    def filter(self, record):
        return super(RequestFilter, self).filter(record)
