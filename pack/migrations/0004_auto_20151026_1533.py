# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0003_auto_20151025_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Serve',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shopId', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\xba\x97\xe9\x93\xbaId')),
                ('telephone', models.CharField(unique=True, max_length=11, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d')),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\xba\x97\xe5\x91\x98\xe5\x90\x8d')),
                ('headImage', models.CharField(max_length=100, verbose_name=b'\xe5\xba\x97\xe5\x91\x98\xe5\xa4\xb4\xe5\x83\x8f')),
                ('status', models.CharField(default=b'0', max_length=1, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u7a7a\u95f2'), ('1', '\u5fd9\u788c'), ('2', '\u79bb\u7ebf')])),
                ('clientID', models.CharField(max_length=40)),
                ('lastLoginTime', models.CharField(default=b'0', max_length=13, verbose_name=b'\xe4\xb8\x8a\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x97\xb6\xe9\x97\xb4')),
                ('deviceToken', models.CharField(default=b'0', max_length=64, verbose_name=b'iOS\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7')),
                ('deviceInfo', models.CharField(default=b'none', max_length=20, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x90\x8d\xe7\xa7\xb0\xef\xbc\x88iOS\xe3\x80\x81Android\xef\xbc\x89')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServeFeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 10, 26, 15, 32, 55, 228000))),
                ('serve', models.ForeignKey(to='pack.Serve')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Waiter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('everSetInfo', models.BooleanField(default=False)),
                ('telephone', models.CharField(unique=True, max_length=11, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d')),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\xba\x97\xe5\x91\x98\xe5\x90\x8d')),
                ('headImage', models.CharField(max_length=100, verbose_name=b'\xe5\xba\x97\xe5\x91\x98\xe5\xa4\xb4\xe5\x83\x8f')),
                ('status', models.CharField(default=b'0', max_length=1, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u7a7a\u95f2'), ('1', '\u5fd9\u788c'), ('2', '\u79bb\u7ebf')])),
                ('clientID', models.CharField(max_length=40)),
                ('lastLoginTime', models.CharField(default=b'0', max_length=13, verbose_name=b'\xe4\xb8\x8a\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x97\xb6\xe9\x97\xb4')),
                ('deviceToken', models.CharField(default=b'0', max_length=64, verbose_name=b'iOS\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7')),
                ('deviceInfo', models.CharField(default=b'none', max_length=20, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x90\x8d\xe7\xa7\xb0\xef\xbc\x88iOS\xe3\x80\x81Android\xef\xbc\x89')),
                ('shop', models.ForeignKey(to='pack.Shop', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WaiterFeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 10, 26, 15, 32, 55, 227000))),
                ('waiter', models.ForeignKey(to='pack.Waiter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='waiterorder',
            name='shop',
        ),
        migrations.RemoveField(
            model_name='waiterorderfeedback',
            name='waiterOrder',
        ),
        migrations.DeleteModel(
            name='WaiterOrder',
        ),
        migrations.DeleteModel(
            name='WaiterOrderFeedBack',
        ),
        migrations.RemoveField(
            model_name='waiterserve',
            name='category',
        ),
        migrations.RemoveField(
            model_name='waiterservefeedback',
            name='waiterServe',
        ),
        migrations.DeleteModel(
            name='WaiterServe',
        ),
        migrations.DeleteModel(
            name='WaiterServeFeedBack',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='waiterOrderId',
            new_name='waiterId',
        ),
        migrations.RenameField(
            model_name='ordersku',
            old_name='waiterServeId',
            new_name='serveId',
        ),
        migrations.RenameField(
            model_name='ordersku',
            old_name='waiterServeName',
            new_name='serveName',
        ),
        migrations.RenameField(
            model_name='orderskubackup',
            old_name='waiterServeId',
            new_name='serveId',
        ),
        migrations.RenameField(
            model_name='orderskubackup',
            old_name='waiterServeName',
            new_name='serveName',
        ),
        migrations.RenameField(
            model_name='table',
            old_name='waiterOrderId',
            new_name='waiterId',
        ),
        migrations.AddField(
            model_name='cook',
            name='everSetInfo',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordersku',
            name='shopId',
            field=models.CharField(default=b'0', max_length=20, verbose_name=b'shopId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderskubackup',
            name='shopId',
            field=models.CharField(default=b'0', max_length=20, verbose_name=b'shopId'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='serveDispatchUnit',
            field=models.PositiveSmallIntegerField(default=1, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x91\x98\xe5\x88\x86\xe9\x85\x8d\xe6\x9c\x80\xe5\xb0\x8f\xe5\x8d\x95\xe4\xbd\x8d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 15, 32, 55, 227000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ordersku',
            name='status',
            field=models.CharField(default=b'0', max_length=3, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u672a\u5904\u7406'), ('2', '\u53a8\u623f\u5904\u7406\u4e2d'), ('4', '\u53a8\u623f\u5df2\u5904\u7406'), ('5', '\u6b63\u5728\u4e0a\u83dc'), ('6', '\u5df2\u4e0a\u83dc'), ('200', '\u53d6\u6d88')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderskubackup',
            name='orderSkuId',
            field=models.CharField(default=b'', unique=True, max_length=20, verbose_name=b'orderSkuId'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderskubackup',
            name='status',
            field=models.CharField(default=b'0', max_length=3, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u672a\u5904\u7406'), ('2', '\u53a8\u623f\u5904\u7406\u4e2d'), ('4', '\u53a8\u623f\u5df2\u5904\u7406'), ('5', '\u6b63\u5728\u4e0a\u83dc'), ('6', '\u5df2\u4e0a\u83dc'), ('200', '\u53d6\u6d88')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 15, 32, 55, 226000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 15, 32, 55, 228000)),
            preserve_default=True,
        ),
    ]
