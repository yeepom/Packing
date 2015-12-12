# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0002_auto_20151025_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderskubackup',
            name='category',
        ),
        migrations.AddField(
            model_name='ordersku',
            name='everSync',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderskubackup',
            name='categoryId',
            field=models.CharField(default=b'0', max_length=20, verbose_name=b'categoryId'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 22, 7, 37, 598000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 22, 7, 37, 597000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 22, 7, 37, 599000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterorderfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 22, 7, 37, 597000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterservefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 22, 7, 37, 599000)),
            preserve_default=True,
        ),
    ]
