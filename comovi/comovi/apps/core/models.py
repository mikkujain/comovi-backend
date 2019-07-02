import os
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from comovi.apps.core.translations import translations
# Create your models here.
from django.utils.timezone import now
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from datetime import datetime
from django import template
from django.db.models import Q
register = template.Library()
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from comovi.common.mail import MailManager
from ckeditor.fields import RichTextField




def get_path_user_profile_picture(instance, filename):
    print(instance)
    return os.path.join('user/profile_pictures/', "%s.%s" % (uuid.uuid4(), filename.split('.')[-1]))


def get_path_media_images(instance, filename):
    print(instance)
    return os.path.join('images/', "%s.%s" % (uuid.uuid4(), filename.split('.')[-1]))


def get_path_media_files(instance, filename):
    print(instance)
    return os.path.join('files/', "%s.%s" % (uuid.uuid4(), filename.split('.')[-1]))


def get_path_post_files(instance, filename):
    print(instance)
    return os.path.join('post/files/', "%s.%s" % (uuid.uuid4(), filename.split('.')[-1]))


def get_path_interior_files(instance, filename):
    print(instance)
    return os.path.join('interiors/files/', "%s.%s" % (uuid.uuid4(), filename.split('.')[-1]))


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Fecha de creación')
    date_modification = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_%(class)ss', editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='updated_%(class)ss', editable=False)

    def save(self, use_save_operations=True, *args, **kwargs):
        self.date_modification = now()
        if not self.date_creation:
            self.date_creation = now()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


# noinspection PyUnresolvedReferences
class PreferenceMixin(object):

    @classmethod
    def get(cls):
        if cls.objects.count() == 0:
            with transaction.atomic():
                instance = cls()
                instance.save()
        return cls.objects.first()


class SitePreferences(BaseModel, PreferenceMixin):
    site_logo = models.ImageField(upload_to=get_path_media_images, null=True, blank=True,
                                  verbose_name=translations['site_logo'])
    site_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=translations['site_name'],
                                 default='BASE_NAME')

    class Meta:
        verbose_name = translations['site_preferences']
        verbose_name_plural = translations['site_preferences']

    def __str__(self):
        return translations['site_preferences']

class CommonEmailTemplate(BaseModel):
    name_of_template = models.CharField(max_length=100, editable=False)
    content = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.name_of_template

class User(AbstractUser, BaseModel):
    MALE = 1
    FEMALE = 2

    GENDER_CHOICES = (
        (MALE, _(translations['male'])),
        (FEMALE, _(translations['female'])),
    )

    first_name = models.CharField(max_length=30, verbose_name=_(translations['first_name']))
    last_name = models.CharField(max_length=30, verbose_name=_(translations['last_name']))
    mother_last_name = models.CharField(max_length=30, verbose_name=_(translations['mother_last_name']), null=True,
                                        blank=True)

    rfc = models.CharField(max_length=13, null=True, blank=True, verbose_name=_(translations['rfc']))
    gender = models.PositiveIntegerField(choices=GENDER_CHOICES, default=FEMALE)
    birth_date = models.DateField(null=True, blank=True,  verbose_name=_(translations['birth_date']))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,10}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=10,null=True, blank=True, verbose_name=_(translations['phone']))
    cell_phone = models.CharField(validators=[phone_regex], max_length=10, null=True, blank=True, verbose_name=_(translations['cell_phone']))
    profile_picture = models.ImageField(
        upload_to=get_path_user_profile_picture,
        null=True,
        blank=True,
        verbose_name=_(translations['profile_picture'])
    )

    class Meta:
        verbose_name = _(translations['user'])
        verbose_name_plural = _(translations['users'])

    def __str__(self):
        return self.username

    def unread_messages(self):
        u = Conversation.objects.filter(user__id=self.id).distinct()
        convs = Conversation.objects.filter(receivers__id__in=[self.id]).distinct()
        admin = Conversation.objects.filter(user=self.id, receivers__id__in=[self.id]).distinct()
        unread = 0
        if hasattr(self, 'owner_profile') and self.owner_profile:
            for con in convs:
                unread += len(con.messages.all().filter(metas__user__id__in=[self.id], metas__is_seen=False).distinct())

        elif hasattr(self, 'admin_profile') and self.admin_profile:
            for con in u:
                unread += len(con.messages.all().filter(metas__user__id__in=[self.id], metas__is_seen=False).distinct())
        
        else:
            for con in admin:
                unread += len(con.messages.all().filter(metas__user__id__in=[self.id], metas__is_seen=False).distinct())

        return unread


    def get_absolute_url(self):
        return reverse("website:my_profile")

    def IsPropertyOwner(self):
        print(AdminProfile.objects.get(user__id=self.id))
        return AdminProfile.objects.get(user__id=self.id)

    def getNewsCount(self):
        if hasattr(self, 'owner_profile') and self.owner_profile:
            return len(Post.objects.filter(seen=False, property__id__in=self.owner_profile.my_properties().values_list('id', flat=True)).order_by('-date_creation'))
        # elif hasattr(self, 'admin_profile') and self.admin_profile:
        #     return len(Post.objects.filter(seen=False, property__id__in=self.admin_profile.my_properties().values_list('id', flat=True)).order_by('-date_creation'))
        else:
            return len(Post.objects.filter(seen=False))

class Property(BaseModel):
    REGISTERED = 1
    MANAGED = 2

    STATUS_CHOICES = (
        (REGISTERED, 'Registrado'),
        (MANAGED, 'Contratado')
    )
    name = models.CharField(max_length=300, verbose_name=translations['name'])
    status = models.IntegerField(choices=STATUS_CHOICES, default=REGISTERED)
    description = models.TextField(blank=False, null=False, default="Fill the description")
    building_picture = models.ImageField(
        upload_to=get_path_user_profile_picture,
        null=True,
        blank=True,
        
    )
    property_logo = models.ImageField(upload_to=get_path_media_images, null=True, blank=True)

    class Meta:
        verbose_name = translations['property']
        verbose_name_plural = translations['properties']   

    def __str__(self):
        return self.name

    def make_preferences(self):
        if not hasattr(self, 'preferences'):
            with transaction.atomic():
                preferences = PropertyPreferences.objects.create(property=self)
                return preferences
        return self.preferences


class AddressProperty(BaseModel):
    property = models.OneToOneField(Property, related_name='address', on_delete=models.CASCADE)
    street = models.CharField(max_length=500, verbose_name=translations['street'])
    exterior_number = models.CharField(max_length=30, verbose_name=translations['exterior_number'], null=True,
                                       blank=True)
    interior_number = models.CharField(max_length=30, blank=True, null=True,
                                       verbose_name=translations['interior_number'])
    colony = models.CharField(max_length=500, null=True, blank=True, verbose_name=translations['colony'])
    zip_code = models.CharField(max_length=20, null=True, blank=True, verbose_name=translations['zip_code'])
    city = models.CharField(max_length=128, null=True, blank=True, verbose_name=translations['city'])
    state = models.CharField(max_length=64, null=True, blank=True, verbose_name=translations['state'])
    reference = models.CharField(max_length=500, null=True, blank=True, verbose_name=translations['reference'])

    class Meta:
        verbose_name = translations['address']
        verbose_name_plural = translations['addresses']


class ContactType(BaseModel):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = translations['contact_type']
        verbose_name_plural = translations['contact_types']


class ContactProperty(BaseModel):
    property = models.ForeignKey(Property, related_name='contacts', on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(ContactType, on_delete=models.SET_NULL, null=True, blank=False,
                             verbose_name=translations['contact_type'])
    name = models.CharField(max_length=100, verbose_name=translations['name'])
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name=translations['phone'])
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name=translations['email'])

    class Meta:
        verbose_name = translations['contact']
        verbose_name_plural = translations['contacts']


class PaymentType(BaseModel):
    name = models.CharField(max_length=100, verbose_name=translations['name'])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = translations['payment_type']
        verbose_name_plural = translations['payment_types']


class CatalogService(BaseModel):
    UNIQUE = 1
    DAILY = 2
    WEEKLY = 3
    BIWEEKLY = 4
    MONTHLY = 5
    YEARLY = 6
    PERIODICITY_CHOICES = (
        (UNIQUE, translations['periodicity_unique']),
        (DAILY, translations['periodicity_daily']),
        (WEEKLY, translations['periodicity_weekly']),
        (BIWEEKLY, translations['periodicity_biweekly']),
        (MONTHLY, translations['periodicity_monthly']),
        (YEARLY, translations['periodicity_yearly'])
    )
    name = models.CharField(max_length=100, verbose_name=translations['name'])
    description = models.TextField(verbose_name=translations['description'], null=True, blank=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, verbose_name=translations['payment_type'],
                                     blank=True, null=True)
    periodicity = models.PositiveIntegerField(choices=PERIODICITY_CHOICES, default=UNIQUE,
                                              verbose_name=translations['periodicity'])

    prepayment_amount = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True,
                                            verbose_name=translations['service_prepayment'])
    payment_amount = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True,
                                         verbose_name=translations['service_payment'])
    untimely_payment_amount = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True,
                                                  verbose_name=translations['service_untimely_payment'])

    can_be_paid_online = models.BooleanField(default=False, verbose_name=translations['can_be_paid_online'])
    payment_link = models.URLField(max_length=500, verbose_name=translations['payment_link'], null=True, blank=True,
                                   help_text=translations['payment_link_help'])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = translations['catalog_service']
        verbose_name_plural = translations['catalog_services']


class PropertyInterior(BaseModel): 
    EMPTY = 1
    OCCUPIED = 2
    STATUS_OCCUPANCY_CHOICES = (
        (EMPTY, translations['status_occupancy_empty']),
        (OCCUPIED, translations['status_occupancy_occupied']),
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name=translations['property'], null=True,
                                 related_name='interiors')
    number = models.CharField(max_length=100, verbose_name=translations['interior_number'])
    resident = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=translations['resident'], null=True,
                                 blank=True)
    status_occupancy = models.PositiveIntegerField(choices=STATUS_OCCUPANCY_CHOICES, default=EMPTY,
                                                   verbose_name=translations['status_occupancy'])


    class Meta:
        verbose_name = translations['property_interior']
        verbose_name_plural = translations['property_interiors']

    def __str__(self):
        return '%s %s' % (self.property.name, self.number)


    def getTotalAmount(self):
        current_month = datetime.now().month
        Phas = self.propertyinteriorhasservice_set.select_related().filter(due_date__month=current_month)
        if Phas:
            print([i.service for i in Phas])
            return sum([i.amount for i in Phas])
        return 0

    def getPaidAmount(self):
        current_month = datetime.now().month
        paid = Payment.objects.filter(property_interior_has_service__in=self.propertyinteriorhasservice_set.select_related().filter(due_date__month=current_month))
        if paid:
            return sum([i.property_interior_has_service.amount for i in paid if i.property_interior_has_service])
        return 0

class PropertyInteriorHasService(BaseModel):
    PENDING = 1
    PENDING_REVIEW = 2
    PAID = 3
    SERVICE_STATUS_CHOICES = (
        (PENDING, translations['service_status_pending']),
        (PENDING_REVIEW, translations['service_status_pending_review']),
        (PAID, translations['service_status_paid']),
    )
    property_interior = models.ForeignKey(PropertyInterior, models.CASCADE, null=True, blank=False,
                                          verbose_name=translations['property_interior'])
    service = models.ForeignKey(CatalogService, on_delete=models.SET_NULL, null=True, blank=False,
                                verbose_name=translations['catalog_service'])
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=translations['amount'], default=0)
    due_date = models.DateField(verbose_name=translations['due_date'])
    invoice = models.FileField(upload_to=get_path_media_files, null=True, blank=True, verbose_name=translations['file'])
    status_payment = models.PositiveIntegerField(choices=SERVICE_STATUS_CHOICES, default=PENDING,
                                                 verbose_name=translations['payment_status'])

    class Meta:
        verbose_name = translations['service']
        verbose_name_plural = translations['services']

    def __str__(self):
        return '{} at {}'.format(self.property_interior, self.service.name)


class Payment(BaseModel):
    property_interior_has_service = models.OneToOneField(PropertyInteriorHasService, on_delete=models.CASCADE,
                                                         verbose_name=translations['property_interior'])
    payment_datetime = models.DateTimeField(verbose_name=translations['payment_datetime'])
    voucher = models.FileField(upload_to=get_path_interior_files, verbose_name=translations['payment_voucher'])
    approval_number = models.CharField(max_length=500, verbose_name=translations['approval_number'], null=True,
                                       blank=True)

    def __str__(self):
        return self.property_interior_has_service.property_interior.number

    class Meta:
        verbose_name = translations['payment']
        verbose_name_plural = translations['payments']


class PropertyPreferences(BaseModel):
    property = models.OneToOneField(Property, related_name='preferences', editable=False, on_delete=models.CASCADE)
    show_stats = models.BooleanField(default=True, verbose_name=translations['show_stats'])
    show_services = models.BooleanField(default=True, verbose_name=translations['show_services'])
    services_to_show = models.ManyToManyField(CatalogService, verbose_name=translations['services_to_show'], blank=True)

    class Meta:
        verbose_name = translations['property_preferences']
        verbose_name_plural = translations['property_preferences']

    def __str__(self):
        return translations['property_preferences']


class Conversation(BaseModel):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY_CHOICES = (
        (HIGH, translations['priority_high']),
        (MEDIUM, translations['priority_medium']),
        (LOW, translations['priority_low'])
    )
    user = models.ForeignKey(User, related_name='conversations', on_delete=models.CASCADE)
    receivers = models.ManyToManyField(User, blank=True, verbose_name=translations['inbox_to'])
    property_interior = models.ForeignKey(PropertyInterior, related_name='conversations', on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, verbose_name=translations['subject'], default='')
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, default=MEDIUM, verbose_name=translations['priority'])


    class Meta:
        ordering = ('-date_creation', '-date_modification')

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('website:conversation', args=(self.id,))

    def get_last_message(self):
        try:
            return self.messages.all()[0]
        except Exception as e:
            pass
        return None


class InboxMessage(BaseModel):
    user = models.ForeignKey(User, related_name='own_messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField(verbose_name=translations['message'], default='Fill in the description')
    
    class Meta:
        ordering = ('-date_creation', 'date_modification')
        verbose_name = translations['message']
        verbose_name_plural = translations['messages']

    def __str__(self):
        return self.message

class MessageMeta(models.Model):
    user = models.ForeignKey(User, related_name='message_metas', on_delete=models.CASCADE)
    message = models.ForeignKey(InboxMessage, related_name='metas', on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False, verbose_name=translations['is_seen'])

    class Meta:
        unique_together = ('user', 'message')

    def __str__(self):  
        return self.user.username


class PostCategory(BaseModel):
    name = models.CharField(max_length=50, verbose_name=translations['post_category_name'])

    class Meta:
        verbose_name = translations['post_category_name']
        verbose_name_plural = translations['post_category_names']

    def __str__(self):
        return self.name


class Post(BaseModel):
    property = models.ForeignKey(Property, related_name='newspaper', null=True, blank=True, on_delete=models.CASCADE,
                                 verbose_name=translations['property'])
    title = models.CharField(max_length=100, verbose_name=translations['post_title'])
    category = models.ForeignKey(PostCategory, verbose_name=translations['post_category_name'],
                                 on_delete=models.SET_NULL, blank=False, null=True)
    cover_image = models.ImageField(upload_to=get_path_post_files, null=True, blank=True,
                                    verbose_name=translations['post_image'])
    seen = models.BooleanField(default=False, verbose_name=translations['seen'])
    body = models.TextField(max_length=1000, verbose_name=translations['post_body'])
    is_active = models.BooleanField(default=True)   

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = translations['post']
        verbose_name_plural = translations['posts']


class PostAttachment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments', verbose_name=translations['post'])
    file = models.FileField(upload_to=get_path_post_files, verbose_name=translations['file'])

    def __str__(self):
        return self.post.title

    class Meta:
        verbose_name = translations['post_attachment']
        verbose_name_plural = translations['post_attachments']


class AdminProfile(BaseModel):
    user = models.OneToOneField(User, related_name='admin_profile', on_delete=models.CASCADE,
                                verbose_name=translations['user'])
    properties_managed = models.ManyToManyField(Property, blank=True, verbose_name=translations['properties_managed'],
                                                related_name='admin_profiles')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = translations['admin_profile']
        verbose_name_plural = translations['admin_profiles']

    def my_owners(self):
        properties = self.properties_managed.all()
        owners = User.objects.none()
        for property in properties:
            for property_interior in property.interiors.all():
                for owner_profile in property_interior.owner_profiles.all():
                    owners |= User.objects.filter(id=owner_profile.user.id)
        return owners

    def my_properties(self):
        properties_managed = self.properties_managed.all()
        properties = Property.objects.none()
        for property_managed in properties_managed:
            properties |= Property.objects.filter(id=property_managed.id)
        return properties


class OwnerProfile(BaseModel):
    user = models.OneToOneField(User, related_name='owner_profile', on_delete=models.CASCADE,
                                verbose_name=translations['user'])
    property_interiors_owned = models.ManyToManyField(PropertyInterior, blank=True,
                                                      verbose_name=translations['property_interiors_owned'],
                                                      related_name='owner_profiles')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = translations['owner_profile']
        verbose_name_plural = translations['owner_profiles']

    def my_admins(self):
        properties = self.property_interiors_owned.all()
        admins = User.objects.none()
        for property_interior in properties:
            property = property_interior.property
            for admin_profile in property.admin_profiles.all():
                admins |= User.objects.filter(id=admin_profile.user.id)
        return admins

    def my_properties(self):
        property_interiors = self.property_interiors_owned.all()
        properties = Property.objects.none()
        for property_interior in property_interiors:
            properties |= Property.objects.filter(id=property_interior.property.id)
        return properties


@receiver(m2m_changed, sender=OwnerProfile.property_interiors_owned.through)
def owner_property_interiors_changed(sender, instance, action, **kwargs):
    if action == 'post_add' and instance.user.email:
        manager = MailManager()
        pk_set = kwargs.pop('pk_set', [])
        prop_interiors = instance.property_interiors_owned.all()
        try:
            data = CommonEmailTemplate.objects.filter(name_of_template='welcome.html')
        except Exception as e:
            print(e)
            return JsonResponse({"status": False})

        for x in data:
            content = x.content
        for new_pk in pk_set:
            inter = prop_interiors.get(pk=new_pk)
            manager.send_welcome(instance.user.email, inter.property.name, '{} {}'.format(instance.user.first_name, instance.user.last_name), content, reverse('website:property', args=(inter.property.id,)))

@receiver(post_save, sender=InboxMessage)
def inbox_message_saved(sender, instance, created, **kwargs):
    if created:
        manager = MailManager()
        conversation = instance.conversation
        try:
            data = CommonEmailTemplate.objects.filter(name_of_template='new_message.html')
        except Exception as e:
            print(e)
            return JsonResponse({"status": False})

        for x in data:
            content = x.content
        for recp in conversation.receivers.all():
            if recp.email:
                manager.send_new_message(recp.email, '{} {}'.format(recp.first_name, recp.last_name), '{} {}'.format(conversation.user.first_name, conversation.user.last_name), \
                 instance.message, content)

@receiver(post_save, sender=Post)
def post_notice_saved(sender, instance, created, **kwargs):
    if created:
        manager = MailManager()
        for prop_inter in instance.property.interiors.all():
            prop_inter_res = prop_inter.resident
            try:
                data = CommonEmailTemplate.objects.filter(name_of_template='new_notice.html')                
            except Exception as e:
                print(e)
                return JsonResponse({"status": False})

            for x in data:
                content = x.content
            if prop_inter_res and prop_inter_res.email:
                manager.send_new_notice(prop_inter_res.email, '{} {}'.format(prop_inter_res.first_name, prop_inter_res.last_name), instance.title, instance.body, content)



