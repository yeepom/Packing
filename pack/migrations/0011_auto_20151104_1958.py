# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0010_auto_20151027_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='waiterName',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe7\x82\xb9\xe8\x8f\x9c\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 4, 19, 58, 48, 168000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 4, 19, 58, 48, 169000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 4, 19, 58, 48, 165000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 4, 19, 58, 48, 170000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 4, 19, 58, 48, 167000)),
            preserve_default=True,
        ),
    ]
