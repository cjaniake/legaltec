# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0012_auto_20160210_0017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentstatus',
            name='minimumValidity',
        ),
    ]
