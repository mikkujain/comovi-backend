# Generated by Django 2.1.7 on 2019-05-23 05:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190515_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressproperty',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_addressproperty', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='addressproperty',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_addressproperty', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='adminprofile',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_adminprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='adminprofile',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_adminprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='catalogservice',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_catalogservice', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='catalogservice',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_catalogservice', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contactproperty',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_contactproperty', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contactproperty',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_contactproperty', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contacttype',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_contacttype', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contacttype',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_contacttype', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_conversation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_conversation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inboxmessage',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_inboxmessage', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inboxmessage',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_inboxmessage', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ownerprofile',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_ownerprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ownerprofile',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_ownerprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_payment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='payment',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_payment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='paymenttype',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_paymenttype', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='paymenttype',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_paymenttype', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_post', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_post', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postattachment',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_postattachment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postattachment',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_postattachment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_postcategory', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_postcategory', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='property',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_property', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='property',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_property', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='propertyinterior',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_propertyinterior', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='propertyinterior',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_propertyinterior', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='propertyinteriorhasservice',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_propertyinteriorhasservice', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='propertyinteriorhasservice',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_propertyinteriorhasservice', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='propertypreferences',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_propertypreferences', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='propertypreferences',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_propertypreferences', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sitepreferences',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_sitepreferences', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sitepreferences',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_sitepreferences', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
