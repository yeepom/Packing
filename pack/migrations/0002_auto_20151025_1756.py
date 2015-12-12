# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='lockDateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 9, 56, 5, 12000, tzinfo=utc), verbose_name=b'\xe6\x97\xa5\xe6\x9c\x9f'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 17, 55, 43, 526000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 17, 55, 43, 525000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 17, 55, 43, 528000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterorderfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 17, 55, 43, 526000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterservefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 17, 55, 43, 527000)),
            preserve_default=True,
        ),
    ]
