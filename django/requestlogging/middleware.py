# -*- coding: utf-8 -*-
import logging

from django_requestlogging.middleware import LogSetupMiddleware as _LogSetupMiddleware

from .logging_filters import RequestFilter

import weakref
weakref_type = type(weakref.ref(lambda: None))


def deref(x):
    return x() if x and type(x) == weakref_type else x


class LogSetupMiddleware(_LogSetupMiddleware):
    FILTER = RequestFilter
