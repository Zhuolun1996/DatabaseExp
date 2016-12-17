# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-15 09:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('Cabinet_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Cabinet_floor', models.CharField(max_length=50)),
                ('Cabinet_position', models.CharField(max_length=50)),
                ('Cabinet_machine_total', models.IntegerField()),
                ('Bandwidth', models.CharField(max_length=50)),
                ('Rest_IP', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cabinet_inner_IP',
            fields=[
                ('Inner_IP_address', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Using_condition', models.CharField(max_length=100)),
                ('Cabinet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlMode.Cabinet')),
            ],
        ),
        migrations.CreateModel(
            name='Cabinet_outer_IP',
            fields=[
                ('Outer_IP_address', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Using_condition', models.CharField(max_length=100)),
                ('Cabinet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlMode.Cabinet')),
            ],
        ),
        migrations.CreateModel(
            name='ComRoom',
            fields=[
                ('Room_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('Room_address', models.CharField(max_length=100)),
                ('IPS', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('Company_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('Contacts', models.CharField(max_length=20)),
                ('PhoneNumber', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Equipments',
            fields=[
                ('PIN_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Model', models.CharField(max_length=50)),
                ('Com_to_switch', models.CharField(max_length=20)),
                ('U_NUM', models.IntegerField()),
                ('Bandwidth', models.CharField(max_length=50)),
                ('Machine_password', models.CharField(max_length=50)),
                ('Using_date', models.DateField()),
                ('Cabinet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlMode.Cabinet')),
                ('Company_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlMode.Customers')),
                ('Inner_IP_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlMode.Cabinet_inner_IP')),
                ('Outer_IP_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlMode.Cabinet_outer_IP')),
            ],
        ),
        migrations.AddField(
            model_name='cabinet',
            name='Room_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlMode.ComRoom'),
        ),
    ]