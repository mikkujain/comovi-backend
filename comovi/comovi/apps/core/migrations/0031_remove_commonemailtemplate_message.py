# Generated by Django 2.1.7 on 2019-05-29 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_commonemailtemplate_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commonemailtemplate',
            name='message',
        ),
    ]
