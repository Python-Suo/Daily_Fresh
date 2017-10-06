# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
        ('df_user', '0002_browsehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBasic',
            fields=[
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('order_id', models.CharField(primary_key=True, help_text='订单id', serialize=False, max_length=64)),
                ('total_count', models.IntegerField(help_text='商品总数', default=1)),
                ('total_price', models.DecimalField(help_text='商品ｚｏｎｇｅ', max_digits=10, decimal_places=2)),
                ('transit_price', models.DecimalField(help_text='订单运费', max_digits=10, decimal_places=2)),
                ('pay_method', models.IntegerField(help_text='支付方式', default=1)),
                ('order_status', models.IntegerField(help_text='订单状态', default=1)),
                ('addr', models.ForeignKey(help_text='收件地址', to='df_user.Address')),
                ('passport', models.ForeignKey(help_text='用户', to='df_user.Passport')),
            ],
            options={
                'db_table': 's_order_basic',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('goods_count', models.IntegerField(help_text='商品数目', default=1)),
                ('goods_price', models.DecimalField(help_text='商品价格', max_digits=10, decimal_places=2)),
                ('goods', models.ForeignKey(help_text='商品', to='df_goods.Goods')),
                ('order', models.ForeignKey(help_text='基本订单', to='df_order.OrderBasic')),
            ],
            options={
                'db_table': 's_order_detail',
            },
        ),
    ]
