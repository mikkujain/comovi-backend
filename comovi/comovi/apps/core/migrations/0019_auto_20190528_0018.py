# Generated by Django 2.1.7 on 2019-05-28 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_emailcondiminium_emailforgetpassword_emailnotice_emailwelcome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailcondiminium',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='emailcondiminium',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='emailforgetpassword',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='emailforgetpassword',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='emailmessage',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='emailmessage',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='emailnotice',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='emailnotice',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='emailwelcome',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='emailwelcome',
            name='modified_by',
        ),
        migrations.DeleteModel(
            name='EmailCondiminium',
        ),
        migrations.DeleteModel(
            name='EmailForgetPassword',
        ),
        migrations.DeleteModel(
            name='EmailMessage',
        ),
        migrations.DeleteModel(
            name='EmailNotice',
        ),
        migrations.DeleteModel(
            name='EmailWelcome',
        ),
    ]
