# -*- coding: utf-8 -*-
import datetime
import uuid

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name=u'作成日時',
                                      auto_now_add=True,
                                      db_index=True)

    updated_at = models.DateTimeField(verbose_name=u'更新日時',
                                      auto_now=True)

    @staticmethod
    def uuid():
        return uuid.uuid4().hex

    @classmethod
    def get_by_pk(cls, pk):
        model = None
        try:
            model = cls.objects.get(pk=pk)
        except ObjectDoesNotExist:
            pass

        return model

    class Meta:
        abstract = True
        app_label = 'common'
        get_latest_by = 'created_at'
        ordering = ['-created_at']


class CacheModel(BaseModel):
    CACHE_KEY = '%s'
    CACHE_TIMEOUT = 5 * 60

    @classmethod
    def get_by_pk(cls, pk):
        key = cls.CACHE_KEY % pk
        model = cache.get(key)

        if model is None:
            try:
                model = cls.objects.get(pk=pk)
                cache.set(key, model, cls.CACHE_TIMEOUT)
            except ObjectDoesNotExist:
                pass

        return model

    def set_cache(self):
        key = self.CACHE_KEY % self.pk
        cache.set(key, self, self.CACHE_TIMEOUT)

        return self

    def delete_cache(self):
        key = self.CACHE_KEY % self.pk
        cache.delete(key)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(CacheModel, self).save(force_insert, force_update, using, update_fields)
        self.set_cache()

        return self

    def delete(self, using=None):
        self.delete_cache()

        super(CacheModel, self).delete(using)

    class Meta(BaseModel.Meta):
        abstract = True
