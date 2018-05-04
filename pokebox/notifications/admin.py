# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import models as auth_models

from . import models


@admin.register(models.Telegram)
class TelegramAdmin(admin.ModelAdmin):
    actions = ['test', 'test_queue']

    def test_queue(self, request, queryset):
        for t in queryset:
            t.notify('Testing 1 2 3...')
    test_queue.short_description = "Test (queue) selected telegrams"

    def test(self, request, queryset):
        for t in queryset:
            m = t.notify('Testing 1 2 3...')
            m.post()
    test.short_description = "Test selected telegrams"


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    actions = ['send']
    list_display = ('channel', 'created', 'sent', 'message')

    def send(self, request, queryset):
        for t in queryset:
            t.post()
    send.short_description = "Send NOW selected messages"