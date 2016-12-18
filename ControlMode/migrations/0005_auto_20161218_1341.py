# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-18 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ControlMode', '0004_auto_20161218_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabinet_inner_ip',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cabinet_inner_ip',
            name='Inner_IP_address',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='cabinet_inner_ip',
            unique_together=set([('Cabinet_id', 'Inner_IP_address')]),
        ),
    ]