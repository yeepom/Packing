# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pack', '0012_auto_20151209_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='AfterCook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('everSetInfo', models.BooleanField(default=False)),
                ('shopId', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\xba\x97\xe9\x93\xbaId')),
                ('telephone', models.CharField(unique=True, max_length=11, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d')),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\xba\x97\xe5\x91\x98\xe5\x90\x8d')),
                ('headImage', models.CharField(max_length=100, verbose_name=b'\xe5\xba\x97\xe5\x91\x98\xe5\xa4\xb4\xe5\x83\x8f')),
                ('status', models.CharField(default=b'0', max_length=1, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u7a7a\u95f2'), ('1', '\u5fd9\u788c'), ('2', '\u79bb\u7ebf')])),
                ('clientID', models.CharField(max_length=40)),
                ('lastLoginTime', models.CharField(default=b'0', max_length=13, verbose_name=b'\xe4\xb8\x8a\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x97\xb6\xe9\x97\xb4')),
                ('deviceToken', models.CharField(default=b'0', max_length=64, verbose_name=b'iOS\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7')),
                ('deviceInfo', models.CharField(default=b'none', max_length=20, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x90\x8d\xe7\xa7\xb0\xef\xbc\x88iOS\xe3\x80\x81Android\xef\xbc\x89')),
                ('category', models.ForeignKey(to='pack.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AfterCookFeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('date', models.DateTimeField(default=datetime.datetime(2016, 1, 10, 12, 53, 53, 459000))),
                ('afterCook', models.ForeignKey(to='pack.AfterCook')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BeforeCook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('everSetInfo', models.BooleanField(default=False)),
                ('shopId', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\xba\x97\xe9\x93\xbaId')),
                ('telephone', models.CharField(unique=True, max_length=11, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d')),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\xba\x97\xe5\x91\x98\xe5\x90\x8d')),
                ('headImage', models.CharField(max_length=100, verbose_name=b'\xe5\xba\x97\xe5\x91\x98\xe5\xa4\xb4\xe5\x83\x8f')),
                ('status', models.CharField(default=b'0', max_length=1, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u7a7a\u95f2'), ('1', '\u5fd9\u788c'), ('2', '\u79bb\u7ebf')])),
                ('clientID', models.CharField(max_length=40)),
                ('lastLoginTime', models.CharField(default=b'0', max_length=13, verbose_name=b'\xe4\xb8\x8a\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x97\xb6\xe9\x97\xb4')),
                ('deviceToken', models.CharField(default=b'0', max_length=64, verbose_name=b'iOS\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7')),
                ('deviceInfo', models.CharField(default=b'none', max_length=20, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x90\x8d\xe7\xa7\xb0\xef\xbc\x88iOS\xe3\x80\x81Android\xef\xbc\x89')),
                ('category', models.ForeignKey(to='pack.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BeforeCookFeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('date', models.DateTimeField(default=datetime.datetime(2016, 1, 10, 12, 53, 53, 459000))),
                ('beforeCook', models.ForeignKey(to='pack.BeforeCook')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderSeparate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('everSetInfo', models.BooleanField(default=False)),
                ('shopId', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\xba\x97\xe9\x93\xbaId')),
                ('telephone', models.CharField(unique=True, max_length=11, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d')),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\xba\x97\xe5\x91\x98\xe5\x90\x8d')),
                ('headImage', models.CharField(max_length=100, verbose_name=b'\xe5\xba\x97\xe5\x91\x98\xe5\xa4\xb4\xe5\x83\x8f')),
                ('status', models.CharField(default=b'0', max_length=1, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u7a7a\u95f2'), ('1', '\u5fd9\u788c'), ('2', '\u79bb\u7ebf')])),
                ('clientID', models.CharField(max_length=40)),
                ('lastLoginTime', models.CharField(default=b'0', max_length=13, verbose_name=b'\xe4\xb8\x8a\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x97\xb6\xe9\x97\xb4')),
                ('deviceToken', models.CharField(default=b'0', max_length=64, verbose_name=b'iOS\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7')),
                ('deviceInfo', models.CharField(default=b'none', max_length=20, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x90\x8d\xe7\xa7\xb0\xef\xbc\x88iOS\xe3\x80\x81Android\xef\xbc\x89')),
                ('category', models.ForeignKey(to='pack.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderSeparateFeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('date', models.DateTimeField(default=datetime.datetime(2016, 1, 10, 12, 53, 53, 458000))),
                ('orderSeparate', models.ForeignKey(to='pack.OrderSeparate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='OrderSkuBackup',
        ),
        migrations.RemoveField(
            model_name='category',
            name='dispatchUnit',
        ),
        migrations.RemoveField(
            model_name='ordersku',
            name='everSync',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='serveDispatchUnit',
        ),
        migrations.RemoveField(
            model_name='table',
            name='isValid',
        ),
        migrations.AddField(
            model_name='category',
            name='categoryType',
            field=models.CharField(default=b'0', max_length=1, choices=[('0', '\u70ed\u83dc'), ('1', '\u51c9\u83dc'), ('2', '\u996e\u54c1')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='userName',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe5\xad\x97'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordersku',
            name='afterCookId',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\x90\x8e\xe6\x89\x93\xe8\x8d\xb7id'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordersku',
            name='afterCookName',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\x90\x8e\xe6\x89\x93\xe8\x8d\xb7\xe5\x90\x8d\xe5\xad\x97'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordersku',
            name='beforeCookId',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\x89\x8d\xe6\x89\x93\xe8\x8d\xb7id'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordersku',
            name='beforeCookName',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\x89\x8d\xe6\x89\x93\xe8\x8d\xb7\xe5\x90\x8d\xe5\xad\x97'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordersku',
            name='categoryType',
            field=models.CharField(default=b'0', max_length=20, verbose_name=b'categoryType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordersku',
            name='orderSeparateId',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe9\x85\x8d\xe8\x8f\x9c\xe5\x91\x98id'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordersku',
            name='orderSeparateName',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe9\x85\x8d\xe8\x8f\x9c\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cookfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 12, 53, 53, 458000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'0', max_length=4, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u5904\u7406\u4e2d'), ('2', '\u5f85\u8bc4\u4ef7'), ('4', '\u5b8c\u6210')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='waiterId',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe7\x82\xb9\xe8\x8f\x9c\xe5\x91\x98id'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ordersku',
            name='status',
            field=models.CharField(default=b'0', max_length=3, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u672a\u5904\u7406'), ('2', '\u914d\u83dc\u4e2d'), ('4', '\u5df2\u914d\u83dc'), ('6', '\u53a8\u5e08\u5904\u7406\u4e2d'), ('8', '\u6b63\u5728\u51fa\u83dc'), ('10', '\u5df2\u4e0a\u83dc'), ('200', '\u53d6\u6d88')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servefeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 12, 53, 53, 460000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 12, 53, 53, 457000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='table',
            name='status',
            field=models.CharField(default=b'0', max_length=1, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u7a7a\u95f2'), ('2', '\u5546\u5bb6\u9501\u5b9a'), ('3', '\u5fd9\u788c')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 12, 53, 53, 460000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waiterfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 12, 53, 53, 457000)),
            preserve_default=True,
        ),
    ]
