# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0015_auto_20160110_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='isValid',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aftercookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 19, 7, 23, 433000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beforecookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 19, 7, 23, 433000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 19, 7, 23, 431000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderseparatefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 19, 7, 23, 432000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 19, 7, 23, 434000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 19, 7, 23, 430000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 19, 7, 23, 434000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 19, 7, 23, 431000)),
            preserve_default=True,
        ),
    ]
