# Generated by Django 2.1.7 on 2019-05-29 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20190529_0403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
    ]