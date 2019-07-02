# Generated by Django 2.1.7 on 2019-05-31 08:55

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_auto_20190531_0245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='content1',
        ),
        migrations.RemoveField(
            model_name='property',
            name='template_name',
        ),
        migrations.AddField(
            model_name='ownerprofile',
            name='content1',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ownerprofile',
            name='template_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.CommonEmailTemplate'),
        ),
    ]
