# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0008_auto_20151026_2340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skusize',
            name='sku',
        ),
        migrations.DeleteModel(
            name='SkuSize',
        ),
        migrations.AddField(
            model_name='sku',
            name='price',
            field=models.CharField(default=1, max_length=200, verbose_name=b'\xe4\xbb\xb7\xe6\xa0\xbc'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='size',
            field=models.CharField(default=2, max_length=200, verbose_name=b'\xe5\x9e\x8b\xe5\x8f\xb7'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 27, 17, 45, 14, 984000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 27, 17, 45, 14, 984000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 27, 17, 45, 14, 982000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 27, 17, 45, 14, 985000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 27, 17, 45, 14, 983000)),
            preserve_default=True,
        ),
    ]
