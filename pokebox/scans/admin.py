# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import models as auth_models

from . import models


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    search_fields = ('mac', 'ip')
    list_display = ('mac', 'name', 'ip', 'last_seen', 'online')


@admin.register(models.DeviceHistory)
class DeviceHistoryAdmin(admin.ModelAdmin):
    list_filter = ('device', 'changed_date', 'field_changed')
    list_display = ('device', 'changed_date', 'field_changed', 'field_old_value', 'field_value')


admin.site.unregister(auth_models.Group)
