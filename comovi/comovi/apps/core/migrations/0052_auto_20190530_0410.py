# Generated by Django 2.1.7 on 2019-05-30 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_auto_20190530_0259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content1',
        ),
        migrations.RemoveField(
            model_name='post',
            name='template_name',
        ),
    ]
