# -*- coding: utf-8 -*-
from ojos.django.core.admin import BaseAdmin


class ConfigAdmin(BaseAdmin):
    list_display = ('key', 'short_value', 'module', 'short_description',)
    ordering = ('key',)
    list_filter = ('module',)
    search_fields = ('key',)

    def short_value(self, obj):
        if len(obj.value) > 30:
            return '%s...' % obj.value[:30]
        else:
            return obj.value
    short_value.short_description = u'値'

    def short_description(self, obj):
        if len(obj.description) > 30:
            return '%s...' % obj.description[:30]
        else:
            return obj.description
    short_description.short_description = u'概要'
