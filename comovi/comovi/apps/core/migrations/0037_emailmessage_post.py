# Generated by Django 2.1.7 on 2019-05-29 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20190529_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmessage',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_notice', to='core.Post'),
        ),
    ]
