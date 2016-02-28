# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('area', '0008_auto_20160210_2244'),
        ('customauth', '0003_systemevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eventDate', models.DateTimeField(auto_now=True)),
                ('readDate', models.DateTimeField(null=True, blank=True)),
                ('subject', models.CharField(max_length=100, verbose_name=b'Assunto')),
                ('text', models.CharField(max_length=1000, verbose_name=b'Texto da mensagem')),
                ('origin', models.IntegerField(default=3, verbose_name=b'Origem', choices=[(1, b'User'), (2, b'Company'), (3, b'System')])),
                ('establishment', models.ForeignKey(verbose_name=b'Estabelecimento', blank=True, to='area.Establishment', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]
