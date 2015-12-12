# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('categoryName', models.CharField(max_length=20)),
                ('dispatchUnit', models.PositiveSmallIntegerField(default=1, verbose_name=b'\xe5\x88\x86\xe9\x85\x8d\xe6\x9c\x80\xe5\xb0\x8f\xe5\x8d\x95\xe4\xbd\x8d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cook',
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
                ('category', models.ForeignKey(to='pack.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CookFeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 10, 25, 17, 15, 4, 939000))),
                ('cook', models.ForeignKey(to='pack.Cook')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shopId', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\xba\x97\xe9\x93\xbaId')),
                ('waiterOrderId', models.CharField(default=b'0', max_length=20, verbose_name=b'\xe7\x82\xb9\xe8\x8f\x9c\xe5\x91\x98id')),
                ('userId', models.CharField(default=b'', max_length=20, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7id')),
                ('tableId', models.CharField(max_length=20, verbose_name=b'\xe9\xa4\x90\xe6\xa1\x8cid')),
                ('tableNumber', models.CharField(max_length=100, verbose_name=b'\xe9\xa4\x90\xe6\xa1\x8c\xe5\x8f\xb7')),
                ('priceTotal', models.DecimalField(verbose_name=b'\xe6\x80\xbb\xe8\xae\xa1', max_digits=8, decimal_places=2)),
                ('status', models.CharField(default=b'0', max_length=4, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u5904\u7406\u4e2d'), ('2', '\u5f85\u4ed8\u6b3e'), ('4', '\u5f85\u8bc4\u4ef7'), ('6', '\u5b8c\u6210')])),
                ('thirdChargeNO', models.CharField(default=b'0', max_length=40, verbose_name=b'\xe7\xac\xac\xe4\xb8\x89\xe6\x96\xb9\xe4\xba\xa4\xe6\x98\x93id')),
                ('note', models.CharField(default=b'', max_length=200, verbose_name=b'\xe8\xae\xb0\xe5\xbd\x95')),
                ('date', models.DateTimeField(verbose_name=b'\xe6\x97\xa5\xe6\x9c\x9f')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record', models.CharField(max_length=200, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('date', models.DateTimeField(verbose_name=b'\xe6\x97\xa5\xe6\x9c\x9f')),
                ('order', models.ForeignKey(to='pack.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderSku',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('categoryId', models.CharField(default=b'0', max_length=20, verbose_name=b'categoryId')),
                ('tableId', models.CharField(max_length=20, verbose_name=b'\xe9\xa4\x90\xe6\xa1\x8cid')),
                ('tableNumber', models.CharField(max_length=100, verbose_name=b'\xe9\xa4\x90\xe6\xa1\x8c\xe5\x8f\xb7')),
                ('skuId', models.CharField(default=b'1', max_length=20, verbose_name=b'skuId')),
                ('skuName', models.CharField(max_length=50, verbose_name=b'sku\xe5\x90\x8d\xe5\xad\x97')),
                ('skuPrice', models.DecimalField(default=1, verbose_name=b'\xe5\x8d\x95\xe4\xbb\xb7', max_digits=6, decimal_places=2)),
                ('skuSizeName', models.CharField(max_length=200, verbose_name=b'\xe5\x9e\x8b\xe5\x8f\xb7')),
                ('skuQuantity', models.PositiveIntegerField(default=0, verbose_name=b'\xe6\x95\xb0\xe9\x87\x8f')),
                ('status', models.CharField(default=b'0', max_length=3, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u672a\u5904\u7406'), ('2', '\u53a8\u623f\u5904\u7406\u4e2d'), ('4', '\u53a8\u623f\u5df2\u5904\u7406'), ('6', '\u5df2\u4e0a\u83dc'), ('200', '\u53d6\u6d88')])),
                ('cookId', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\x8e\xa8\xe5\xb8\x88id')),
                ('cookName', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\x8e\xa8\xe5\xb8\x88\xe5\x90\x8d\xe5\xad\x97')),
                ('waiterServeId', models.CharField(default=b'', max_length=20, verbose_name=b'\xe4\xb8\x8a\xe8\x8f\x9c\xe5\x91\x98id')),
                ('waiterServeName', models.CharField(default=b'', max_length=20, verbose_name=b'\xe4\xb8\x8a\xe8\x8f\x9c\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97')),
                ('order', models.ForeignKey(to='pack.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderSkuBackup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orderSkuId', models.CharField(default=b'', max_length=20, verbose_name=b'orderSkuId')),
                ('tableId', models.CharField(max_length=20, verbose_name=b'\xe9\xa4\x90\xe6\xa1\x8cid')),
                ('tableNumber', models.CharField(max_length=100, verbose_name=b'\xe9\xa4\x90\xe6\xa1\x8c\xe5\x8f\xb7')),
                ('skuId', models.CharField(default=b'1', max_length=20, verbose_name=b'skuId')),
                ('skuName', models.CharField(max_length=50, verbose_name=b'sku\xe5\x90\x8d\xe5\xad\x97')),
                ('skuPrice', models.DecimalField(default=1, verbose_name=b'\xe5\x8d\x95\xe4\xbb\xb7', max_digits=6, decimal_places=2)),
                ('skuSizeName', models.CharField(max_length=200, verbose_name=b'\xe5\x9e\x8b\xe5\x8f\xb7')),
                ('skuQuantity', models.PositiveIntegerField(default=0, verbose_name=b'\xe6\x95\xb0\xe9\x87\x8f')),
                ('status', models.CharField(default=b'0', max_length=3, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u672a\u5904\u7406'), ('2', '\u53a8\u623f\u5904\u7406\u4e2d'), ('4', '\u53a8\u623f\u5df2\u5904\u7406'), ('6', '\u5df2\u4e0a\u83dc'), ('200', '\u53d6\u6d88')])),
                ('cookId', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\x8e\xa8\xe5\xb8\x88id')),
                ('cookName', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\x8e\xa8\xe5\xb8\x88\xe5\x90\x8d\xe5\xad\x97')),
                ('waiterServeId', models.CharField(default=b'', max_length=20, verbose_name=b'\xe4\xb8\x8a\xe8\x8f\x9c\xe5\x91\x98id')),
                ('waiterServeName', models.CharField(default=b'', max_length=20, verbose_name=b'\xe4\xb8\x8a\xe8\x8f\x9c\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97')),
                ('category', models.ForeignKey(to='pack.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('setInfoStatus', models.CharField(default=b'0', max_length=1, verbose_name=b'\xe8\xae\xbe\xe7\xbd\xae\xe5\x95\x86\xe5\xae\xb6\xe4\xbf\xa1\xe6\x81\xaf\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u6ca1\u6709\u8bbe\u7f6e\u8fc7\u57fa\u672c\u4fe1\u606f'), ('1', '\u6ca1\u6709\u8bbe\u7f6e\u8fc7\u94b1\u5305\u4fe1\u606f'), ('2', '\u8bbe\u7f6e\u5b8c\u6bd5')])),
                ('telephone', models.CharField(unique=True, max_length=11, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d')),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\xba\x97\xe9\x93\xba\xe5\x90\x8d')),
                ('headImage', models.CharField(max_length=100, verbose_name=b'\xe5\xba\x97\xe9\x93\xba\xe5\xa4\xb4\xe5\x83\x8f')),
                ('shopType', models.CharField(default=b'0', max_length=2, verbose_name=b'\xe5\x95\x86\xe5\xae\xb6\xe7\xb1\xbb\xe5\x9e\x8b', choices=[('0', '\u5feb\u9910'), ('1', '\u7092\u83dc'), ('2', '\u706b\u9505'), ('3', '\u5496\u5561'), ('100', '\u5176\u4ed6')])),
                ('desc', models.CharField(default=b'0', max_length=200, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('isServiceOn', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x9c\xa8\xe7\xba\xbf\xe6\x9c\x8d\xe5\x8a\xa1')),
                ('startTimeStamp', models.PositiveSmallIntegerField(default=0, max_length=10, verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3')),
                ('endTimeStamp', models.PositiveSmallIntegerField(default=0, max_length=10, verbose_name=b'\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3')),
                ('star', models.PositiveSmallIntegerField(default=5, verbose_name=b'\xe8\xaf\x84\xe4\xbb\xb7')),
                ('province', models.CharField(default=b'', max_length=20, verbose_name=b'\xe7\x9c\x81\xe4\xbb\xbd')),
                ('city', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\x9f\x8e\xe5\xb8\x82')),
                ('district', models.CharField(default=b'', max_length=20, verbose_name=b'\xe5\x9c\xb0\xe5\x8c\xba')),
                ('addressDetail', models.CharField(default=b'', max_length=100, verbose_name=b'\xe8\xaf\xa6\xe7\xbb\x86\xe4\xbf\xa1\xe6\x81\xaf')),
                ('clientID', models.CharField(default=b'000', max_length=40)),
                ('deviceToken', models.CharField(default=b'0', max_length=64, verbose_name=b'iOS\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7')),
                ('deviceInfo', models.CharField(default=b'', max_length=20, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x90\x8d\xe7\xa7\xb0\xef\xbc\x88iOS\xe3\x80\x81Android\xef\xbc\x89')),
                ('lastLoginTime', models.CharField(default=b'0', max_length=13, verbose_name=b'\xe4\xb8\x8a\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x97\xb6\xe9\x97\xb4')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, null=True, verbose_name='longitude/latitude', blank=True)),
            ],
            options={
                'verbose_name': '\u5546\u5bb6',
                'verbose_name_plural': '\u5546\u5bb6\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopEvaluate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('star', models.PositiveSmallIntegerField(verbose_name=b'\xe8\xaf\x84\xe4\xbb\xb7')),
                ('date', models.DateTimeField(verbose_name=b'\xe6\x97\xa5\xe6\x9c\x9f')),
                ('shop', models.ForeignKey(to='pack.Shop')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopFeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 10, 25, 17, 15, 4, 938000))),
                ('shop', models.ForeignKey(to='pack.Shop')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopWallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('realName', models.CharField(default=b'0', max_length=20, verbose_name=b'\xe5\x90\x8d\xe5\xad\x97')),
                ('cardNumber', models.CharField(default=b'0', max_length=19, verbose_name=b'\xe5\x8d\xa1\xe5\x8f\xb7')),
                ('cardType', models.CharField(default=b'0', max_length=1, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', choices=[('0', '\u94f6\u884c\u5361'), ('1', '\u652f\u4ed8\u5b9d\u8d26\u6237')])),
                ('moneyLeft', models.DecimalField(default=0, verbose_name=b'\xe4\xbd\x99\xe9\xa2\x9d', max_digits=7, decimal_places=2)),
                ('moneyTotal', models.DecimalField(default=0, verbose_name=b'\xe7\xb4\xaf\xe8\xae\xa1\xe6\x94\xb6\xe5\x85\xa5', max_digits=7, decimal_places=2)),
                ('moneyTotalOnPlatform', models.DecimalField(default=0, verbose_name=b'\xe5\xb9\xb3\xe5\x8f\xb0\xe7\xb4\xaf\xe8\xae\xa1\xe6\x94\xb6\xe5\x85\xa5', max_digits=7, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sku',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\x90\x8d\xe5\xad\x97')),
                ('desc', models.CharField(max_length=200, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('img', models.CharField(max_length=500, verbose_name=b'\xe5\x9b\xbe\xe5\x83\x8f')),
                ('isValid', models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x9c\x89\xe6\x95\x88')),
                ('category', models.ForeignKey(to='pack.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkuSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'\xe5\xb8\xb8\xe8\xa7\x84', max_length=200, verbose_name=b'\xe5\x9e\x8b\xe5\x8f\xb7')),
                ('price', models.DecimalField(default=1, verbose_name=b'\xe5\x8d\x95\xe4\xbb\xb7', max_digits=6, decimal_places=2)),
                ('sku', models.ForeignKey(to='pack.Sku')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=100, verbose_name=b'\xe5\x8f\xb7\xe7\xa0\x81')),
                ('peopleNumber', models.PositiveSmallIntegerField(default=2, verbose_name=b'\xe5\xae\xb9\xe7\xba\xb3\xe4\xba\xba\xe6\x95\xb0')),
                ('status', models.CharField(default=b'0', max_length=1, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[('0', '\u7a7a\u95f2'), ('1', '\u7528\u6237\u9501\u5b9a'), ('2', '\u5546\u5bb6\u9501\u5b9a'), ('3', '\u5fd9\u788c')])),
                ('isValid', models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x9c\x89\xe6\x95\x88')),
                ('userId', models.CharField(default=b'0', max_length=20, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7id')),
                ('waiterOrderId', models.CharField(default=b'0', max_length=20, verbose_name=b'\xe7\x82\xb9\xe8\x8f\x9c\xe5\x91\x98id')),
                ('shop', models.ForeignKey(to='pack.Shop')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransferMoney',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total', models.DecimalField(verbose_name=b'\xe9\x87\x91\xe9\xa2\x9d', max_digits=8, decimal_places=2)),
                ('startDateString', models.CharField(max_length=40, verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xa5\xe6\x9c\x9f')),
                ('endDateString', models.CharField(max_length=40, verbose_name=b'\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xa5\xe6\x9c\x9f')),
                ('date', models.DateTimeField(verbose_name=b'\xe6\x97\xa5\xe6\x9c\x9f')),
                ('shop', models.ForeignKey(to='pack.Shop')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telephone', models.CharField(unique=True, max_length=11, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d')),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe6\x98\xb5\xe7\xa7\xb0')),
                ('headImage', models.CharField(max_length=100, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('clientID', models.CharField(max_length=40)),
                ('lastLoginTime', models.CharField(default=b'0', max_length=13, verbose_name=b'\xe4\xb8\x8a\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x97\xb6\xe9\x97\xb4')),
                ('deviceToken', models.CharField(default=b'0', max_length=64, verbose_name=b'iOS\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7')),
                ('deviceInfo', models.CharField(default=b'none', max_length=20, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x90\x8d\xe7\xa7\xb0\xef\xbc\x88iOS\xe3\x80\x81Android\xef\xbc\x89')),
            ],
            options={
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserFeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 10, 25, 17, 15, 4, 940000))),
                ('user', models.ForeignKey(to='pack.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WaiterOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            name='WaiterOrderFeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 10, 25, 17, 15, 4, 939000))),
                ('waiterOrder', models.ForeignKey(to='pack.WaiterOrder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WaiterServe',
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
                ('category', models.ForeignKey(to='pack.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WaiterServeFeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 10, 25, 17, 15, 4, 940000))),
                ('waiterServe', models.ForeignKey(to='pack.WaiterServe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='shopevaluate',
            name='user',
            field=models.ForeignKey(to='pack.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='shopwallet',
            field=models.OneToOneField(null=True, to='pack.ShopWallet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='shop',
            field=models.ForeignKey(to='pack.Shop'),
            preserve_default=True,
        ),
    ]
