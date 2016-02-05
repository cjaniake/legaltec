# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'\xc3\x81rea')),
                ('adminEmail', models.EmailField(max_length=254, verbose_name=b'Email administrador')),
            ],
        ),
        migrations.CreateModel(
            name='AreaStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'Status')),
                ('enabled', models.BooleanField(verbose_name=b'Ativo')),
            ],
        ),
        migrations.CreateModel(
            name='Establishment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name=b'Estabelecimento')),
                ('city', models.CharField(unique=True, max_length=100, verbose_name=b'Cidade')),
                ('state', models.CharField(max_length=2, verbose_name=b'Estado')),
                ('adminEmail', models.EmailField(max_length=254, verbose_name=b'Email administrador')),
                ('area', models.ForeignKey(verbose_name=b'\xc3\x81rea', to='area.Area')),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='areaStatus',
            field=models.ForeignKey(verbose_name=b'Status', to='area.AreaStatus'),
        ),
        migrations.AlterUniqueTogether(
            name='establishment',
            unique_together=set([('area', 'name')]),
        ),
    ]
