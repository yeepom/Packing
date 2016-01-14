# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0018_auto_20160110_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serve',
            name='shop',
        ),
        migrations.AddField(
            model_name='serve',
            name='shopId',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\xba\x97\xe9\x93\xbaId'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aftercookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 20, 25, 18, 512000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beforecookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 20, 25, 18, 512000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 20, 25, 18, 512000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderseparatefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 20, 25, 18, 512000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 20, 25, 18, 512000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 20, 25, 18, 512000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 20, 25, 18, 512000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 20, 25, 18, 512000)),
            preserve_default=True,
        ),
    ]
