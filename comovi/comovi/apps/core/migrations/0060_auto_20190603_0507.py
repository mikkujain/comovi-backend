# Generated by Django 2.1.7 on 2019-06-03 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_auto_20190603_0503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertyinterior',
            name='content1',
        ),
        migrations.RemoveField(
            model_name='propertyinterior',
            name='template_name',
        ),
    ]
