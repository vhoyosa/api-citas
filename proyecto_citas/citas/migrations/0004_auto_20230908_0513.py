# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2023-09-08 05:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0003_auto_20230901_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citas.Cliente')),
                ('estilista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citas.Estilista')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citas.Servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_rol', models.CharField(choices=[('cliente', 'cliente'), ('admin', 'admin')], max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='roles',
            field=models.ManyToManyField(related_name='roles_asignados', to='citas.Rol'),
        ),
        migrations.AlterUniqueTogether(
            name='reserva',
            unique_together=set([('servicio', 'estilista', 'cliente', 'fecha', 'hora_inicio', 'hora_fin')]),
        ),
    ]