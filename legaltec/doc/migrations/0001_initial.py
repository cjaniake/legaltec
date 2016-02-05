# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'Tipo de documento')),
                ('validityPeriod', models.IntegerField(verbose_name=b'Validade em meses')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentTypeField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'Campo')),
                ('field_type', models.IntegerField(default=1, verbose_name=b'Tipo do campo', choices=[(1, b'Texto'), (2, b'Inteiro'), (3, b'Decimal'), (4, b'Lista')])),
                ('field_choices', models.CharField(max_length=50, verbose_name=b'Op\xc3\xa7\xc3\xb5es')),
                ('documentType', models.ForeignKey(verbose_name=b'Tipo de documento', to='doc.DocumentType')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='documenttypefield',
            unique_together=set([('documentType', 'name')]),
        ),
    ]
