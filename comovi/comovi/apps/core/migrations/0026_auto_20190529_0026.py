# Generated by Django 2.1.7 on 2019-05-29 05:26

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20190528_0713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selectemail',
            name='description',
        ),
        migrations.AddField(
            model_name='selectemail',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
