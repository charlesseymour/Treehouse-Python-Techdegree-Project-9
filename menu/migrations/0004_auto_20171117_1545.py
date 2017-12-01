# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-17 21:45
from __future__ import unicode_literals

from django.db import migrations


def datetime_to_date(apps, schema_editor):
    Menu = apps.get_model('menu', 'Menu')
    for menu in Menu.objects.all():
        menu.new_created_date = menu.created_date.date()
        if menu.expiration_date:
            menu.new_expiration_date = menu.expiration_date.date()
        menu.save()

    Item = apps.get_model('menu', 'Item')
    for item in Item.objects.all():
        item.new_created_date = item.created_date.date()
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20171117_1543'),
    ]

    operations = [
        migrations.RunPython(datetime_to_date)
    ]
