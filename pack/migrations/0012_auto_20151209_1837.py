# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0011_auto_20151104_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 9, 18, 37, 47, 177000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 9, 18, 37, 47, 177000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='shopType',
            field=models.CharField(default=b'0', max_length=2, verbose_name=b'\xe5\x95\x86\xe5\xae\xb6\xe7\xb1\xbb\xe5\x9e\x8b', choices=[('0', '\u5feb\u9910'), ('1', '\u7092\u83dc'), ('2', '\u706b\u9505'), ('3', '\u5496\u5561'), ('10', '\u5176\u4ed6')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 9, 18, 37, 47, 175000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 9, 18, 37, 47, 178000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 9, 18, 37, 47, 176000)),
            preserve_default=True,
        ),
    ]
