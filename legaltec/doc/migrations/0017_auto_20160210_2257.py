# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0016_auto_20160210_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenthistory',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='documenttypefield',
            name='name',
            field=models.CharField(max_length=50, verbose_name=b'Campo'),
        ),
    ]
