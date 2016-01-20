# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0019_auto_20160110_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aftercook',
            name='clientID',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aftercookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 19, 17, 24, 370000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beforecook',
            name='clientID',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beforecookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 19, 17, 24, 369000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cook',
            name='clientID',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 19, 17, 24, 368000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderseparate',
            name='clientID',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderseparatefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 19, 17, 24, 368000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='serve',
            name='clientID',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 19, 17, 24, 371000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='clientID',
            field=models.CharField(default=b'000', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 19, 17, 24, 366000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='clientID',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 19, 17, 24, 371000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiter',
            name='clientID',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 19, 17, 24, 367000)),
            preserve_default=True,
        ),
    ]
