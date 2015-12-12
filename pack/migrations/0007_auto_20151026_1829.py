# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0006_auto_20151026_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderskubackup',
            name='orderId',
            field=models.CharField(default=b'0', max_length=20, verbose_name=b'orderId'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 18, 29, 39, 478000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 18, 29, 39, 479000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 18, 29, 39, 477000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 18, 29, 39, 479000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 18, 29, 39, 478000)),
            preserve_default=True,
        ),
    ]
