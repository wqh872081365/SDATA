# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxy',
            name='anonymity',
            field=models.CharField(choices=[('-1', 'unknown'), ('0', '透明'), ('1', '匿名'), ('2', '高匿')], db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='proxy',
            name='http',
            field=models.CharField(choices=[('-1', 'unknown'), ('0', 'http'), ('1', 'https'), ('2', 'socks4'), ('3', 'socks5')], db_index=True, max_length=255),
        ),
    ]
