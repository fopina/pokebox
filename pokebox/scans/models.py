# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms.models import model_to_dict


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])


class Device(ModelDiffMixin, models.Model):
    mac = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=50, null=True)
    ip = models.CharField(max_length=20)
    last_seen = models.DateTimeField(auto_now_add=True)
    online = models.BooleanField(default=False, db_index=True)

    # set to None for all
    audit_fields = None

    def __unicode__(self):
        return '%s (%s%s)' % (
        	self.mac,
        	self.ip,
        	' - %s' % self.name if self.name else ''
        )

    def save(self, *args, **kwargs):
        diff = self.diff
        create_mode = not self.pk

        super(Device, self).save(*args, **kwargs)

        if create_mode:
            h = DeviceHistory()
            h.device = self
            h.field_changed = '_'
            h.field_value = 'Creation'
            h.save()
        else:
            for field in diff:
                if not self.audit_fields or field in self.audit_fields:
                    h = DeviceHistory()
                    h.device = self
                    h.field_changed = field
                    h.field_value = str(diff[field][1])
                    h.field_old_value = str(diff[field][0])
                    h.save()


class DeviceHistory(models.Model):
    device = models.ForeignKey(Device, db_index=True)
    changed_date = models.DateTimeField(auto_now_add=True)
    field_changed = models.CharField(max_length=10)
    field_value = models.CharField(max_length=50, null=True)
    field_old_value = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return '%s: %s - %s => %s' % (self.device, self.field_changed, self.field_old_value, self.field_value)

    class Meta:
    	verbose_name = 'Device History'
    	verbose_name_plural = 'Device History'