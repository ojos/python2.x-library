# -*- coding: utf-8 -*-
from django.db import models

from ojos.django.core.models import CacheModel


class Config(CacheModel):
    CACHE_KEY = 'config/%s'

    key = models.CharField(verbose_name=u'変数名',
                           primary_key=True,
                           unique=True,
                           db_index=True,
                           max_length=255)

    value = models.TextField(verbose_name=u'値',
                             blank=True,
                             default='')

    module = models.CharField(verbose_name=u'出力時の変換型',
                              max_length=255,
                              default='unicode')

    description = models.CharField(verbose_name=u'概要',
                                   max_length=255,
                                   blank=True,
                                   default='')

    def __unicode__(self):
        return u'%s' % self.key

    class Meta(CacheModel.Meta):
        abstract = True
        verbose_name = verbose_name_plural = u'共通変数'
