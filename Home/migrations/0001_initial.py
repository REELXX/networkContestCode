# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2021-08-16 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserINFO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('email', models.EmailField(max_length=32, verbose_name='邮箱')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('IsVIP', models.BooleanField(default=False)),
            ],
        ),
    ]