# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0020_auto_20160116_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aftercookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 11, 11, 31, 164000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beforecookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 11, 11, 31, 163000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='categoryType',
            field=models.CharField(default=b'0', max_length=1, choices=[('0', '\u70ed\u83dc'), ('1', '\u70ed\u83dc\u65e0\u524d\u6253\u8377'), ('2', '\u51c9\u83dc'), ('3', '\u996e\u54c1')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 11, 11, 31, 156000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderseparatefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 11, 11, 31, 159000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 11, 11, 31, 166000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 11, 11, 31, 155000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 11, 11, 31, 167000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 11, 11, 31, 155000)),
            preserve_default=True,
        ),
    ]
