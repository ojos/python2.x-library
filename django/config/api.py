# -*- coding: utf-8 -*-
from django.conf import settings

from ojos.misc.utils import lazy_loader
from ojos.misc.validators import (validate_list, validate_datetime, validate_time,
                                  validate_timedelta, validate_int, validate_value,
                                  validate_dict)


class ConfigApi(object):
    def __init__(self, model_cls):
        self._model_cls = model_cls

    def get(self, key):
        model = self._model_cls.get_by_pk(key)
        if model is None:
            if key in settings.DEFAULT_CONFIG:
                model = self._model_cls(key=key,
                                        **settings.DEFAULT_CONFIG[key])
                model.save()
            else:
                raise

        try:
            if model.module == 'datetime':
                _value = validate_datetime(validate_list(model.value))
            elif model.module == 'timedelta<list>':
                _value = validate_timedelta(validate_list(model.value))
            elif model.module == 'timedelta<dict>':
                _value = validate_timedelta(validate_dict(model.value))
            elif model.module == 'time':
                _value = validate_time(validate_list(model.value))
            elif model.module == 'list':
                _value = validate_list(model.value)
            elif model.module == 'list<int>':
                _value = validate_list(model.value, validate=validate_int)
            elif model.module == 'dict':
                _value = validate_dict(model.value)
            else:
                try:
                    _module = validate_value(model.module)
                except:
                    _module = lazy_loader(model.module)
                _value = _module(model.value)
        except:
            _value = model.value

        return _value

    def set(self, key, value, module='unicode', description=''):
        model = self._model_cls(key=key,
                                value=value,
                                module=module,
                                description=description)
        model.save()

    def update(self, key, *args, **kwargs):
        model = self._model_cls.get_by_pk(key)
        if model is None:
            if key in settings.DEFAULT_CONFIG:
                model = self._model_cls(key=key,
                                        **settings.DEFAULT_CONFIG[key])
            else:
                raise

        for k, v in dict(*args, **kwargs).items():
            setattr(model, k, v)

        model.save()
        return model

    def reload(self):
        for key in settings.DEFAULT_CONFIG.keys():
            model = self._model_cls.get_by_pk(key)
            if model is not None:
                model.delete_cache()
            self.get(key)
