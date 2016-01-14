# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0014_auto_20160110_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aftercookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 56, 21, 964000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beforecookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 56, 21, 962000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 56, 21, 961000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderseparatefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 56, 21, 962000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 56, 21, 964000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='deviceToken',
            field=models.CharField(default=b'0', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 56, 21, 960000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 56, 21, 965000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 14, 56, 21, 960000)),
            preserve_default=True,
        ),
    ]
