# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import requests


class Telegram(models.Model):
    token = models.CharField(max_length=50, unique=True)
    chat_id = models.IntegerField()
    name = models.CharField(max_length=50, editable=False)
    
    def __unicode__(self):
        return '%s @ %s' % (
            self.name if self.name else self.token,
            self.chat_id
        )

    def notify(self, message):
        return Message.objects.create(channel=self, message=message)
    

class Message(models.Model):
    channel = models.ForeignKey(Telegram, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    sent = models.DateTimeField(null=True, blank=True, editable=False, db_index=True)
    message = models.TextField(editable=False)

    def post(self):
        ret = requests.post(
            'https://api.telegram.org/bot%s/sendMessage' % self.channel.token,
                data={
                    'chat_id': self.channel.chat_id,
                    'text': self.message,
                }
            ).json()

        if ret['ok'] == True:
            if not self.channel.name  and ret['result']['from']['username']:
                self.channel.name = ret['result']['from']['username']
                self.channel.save()
            self.sent = timezone.now()
            self.save()
            return True

        return ret
