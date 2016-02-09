# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0006_document_documenthistory_documentimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('documentFile', models.FileField(upload_to=b'uploads/%Y/%m/%d/')),
                ('uploadDate', models.DateTimeField(auto_now_add=True)),
                ('checksum', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentImageFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imageFile', models.ImageField(upload_to=b'uploads/%Y/%m/%d/')),
                ('uploadDate', models.DateTimeField(auto_now_add=True)),
                ('checksum', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='documentimage',
            name='document',
        ),
        migrations.RenameField(
            model_name='documenttypefield',
            old_name='field_choices',
            new_name='fieldChoices',
        ),
        migrations.RenameField(
            model_name='documenttypefield',
            old_name='field_type',
            new_name='fieldType',
        ),
        migrations.AddField(
            model_name='document',
            name='createdDate',
            field=models.DateField(default=datetime.datetime(2016, 2, 9, 2, 27, 3, 912056, tzinfo=utc), verbose_name=b'Criado', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='modifiedDate',
            field=models.DateField(default=datetime.datetime(2016, 2, 9, 2, 27, 11, 93265, tzinfo=utc), verbose_name=b'Criado', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documenthistory',
            name='eventDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 9, 2, 27, 14, 222088, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DocumentImage',
        ),
        migrations.AddField(
            model_name='documentimagefile',
            name='document',
            field=models.ForeignKey(verbose_name=b'Documento', to='doc.Document'),
        ),
        migrations.AddField(
            model_name='documentfile',
            name='document',
            field=models.ForeignKey(verbose_name=b'Documento', to='doc.Document'),
        ),
    ]
