# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0009_auto_20151027_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 27, 17, 46, 1, 841000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 27, 17, 46, 1, 841000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 27, 17, 46, 1, 840000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sku',
            name='size',
            field=models.CharField(default=b'\xe5\xb8\xb8\xe8\xa7\x84', max_length=200, verbose_name=b'\xe5\x9e\x8b\xe5\x8f\xb7'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 27, 17, 46, 1, 842000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 27, 17, 46, 1, 840000)),
            preserve_default=True,
        ),
    ]
