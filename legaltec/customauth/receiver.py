# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import serializers

from customauth.models import SystemEvent


@receiver(post_save)
def handle_post_save(sender, instance, created, **kwargs):
    if instance.__module__ in ['customauth.models', 'area.models', 'doc.models']:
        evt = SystemEvent();
        evt.entity = instance.__class__.__name__
        evt.operation = 'SAVE'
        evt.snapshot = serializers.serialize("json", [instance, ])
        evt.error = False

        evt.save()