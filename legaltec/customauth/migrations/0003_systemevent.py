# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customauth', '0002_auto_20160208_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eventDate', models.DateTimeField(auto_now_add=True)),
                ('entity', models.CharField(max_length=50, verbose_name=b'Entidade')),
                ('operation', models.CharField(max_length=50, verbose_name=b'Opera\xc3\xa7\xc3\xa3o')),
                ('snapshot', models.CharField(max_length=1000, verbose_name=b'Resumo dos dados')),
                ('error', models.BooleanField(default=False, verbose_name=b'Erro')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
