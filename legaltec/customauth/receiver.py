# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core import serializers

from customauth.models import SystemEvent
import threading
from threadlocals.threadlocals import get_current_user

@receiver(post_save)
def handle_post_save(sender, instance, created, **kwargs):
    if instance.__module__ in ['customauth.models', 'area.models', 'doc.models'] and \
            not instance.__class__.__name__ in ['SystemEvent']:
        evt = SystemEvent();
        evt.entity = instance.__class__.__name__
        evt.operation = 'SAVE'
        evt.snapshot = serializers.serialize("json", [instance, ])
        evt.error = False

        evt.user = get_current_user()

        evt.save()

@receiver(pre_delete)
def handle_pre_delete(sender, instance, created, **kwargs):
    if instance.__module__ in ['customauth.models', 'area.models', 'doc.models']:
        evt = SystemEvent();
        evt.entity = instance.__class__.__name__
        evt.operation = 'DELETE'
        evt.snapshot = serializers.serialize("json", [instance, ])
        evt.error = False

        evt.user = get_current_user()

        evt.save()