# Generated by Django 2.1.7 on 2019-05-29 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20190529_0355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailmessage',
            name='property_interior',
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='prop_inter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_notice', to='core.Post'),
        ),
    ]