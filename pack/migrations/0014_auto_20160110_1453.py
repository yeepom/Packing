# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0013_auto_20160110_1253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='setInfoStatus',
        ),
        migrations.AddField(
            model_name='shop',
            name='everSetInfo',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aftercookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 53, 27, 278000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beforecookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 53, 27, 277000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 53, 27, 275000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderseparatefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 53, 27, 276000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 53, 27, 278000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 53, 27, 273000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 53, 27, 283000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 53, 27, 274000)),
            preserve_default=True,
        ),
    ]
