# Generated by Django 2.1.7 on 2019-05-30 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_commonemailtemplate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selectemail',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='selectemail',
            name='email_template',
        ),
        migrations.RemoveField(
            model_name='selectemail',
            name='modified_by',
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='template_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.CommonEmailTemplate'),
        ),
        migrations.DeleteModel(
            name='SelectEmail',
        ),
    ]
