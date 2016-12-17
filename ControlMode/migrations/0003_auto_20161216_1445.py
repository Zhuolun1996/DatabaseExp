# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-16 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ControlMode', '0002_auto_20161216_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipments',
            name='Intface_to_switch',
            field=models.CharField(choices=[('F 0/0', 'FastEthernet 0/0'), ('F 0/1', 'FastEthernet 0/1'), ('F 0/2', 'FastEthernet 0/2'), ('F 0/3', 'FastEthernet 0/3'), ('F 0/4', 'FastEthernet 0/4'), ('F 0/5', 'FastEthernet 0/5'), ('F 0/6', 'FastEthernet 0/6'), ('F 0/7', 'FastEthernet 0/7'), ('F 0/8', 'FastEthernet 0/8'), ('F 0/9', 'FastEthernet 0/9'), ('F 0/10', 'FastEthernet 0/10'), ('F 0/11', 'FastEthernet 0/11')], max_length=20),
        ),
    ]
