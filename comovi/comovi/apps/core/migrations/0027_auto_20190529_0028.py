# Generated by Django 2.1.7 on 2019-05-29 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20190529_0026'),
    ]

    operations = [
        migrations.RenameField(
            model_name='selectemail',
            old_name='name_of_template',
            new_name='name',
        ),
    ]
