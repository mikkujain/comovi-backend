# Generated by Django 2.1.7 on 2019-05-28 05:20

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20190528_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]