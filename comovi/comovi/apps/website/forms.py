from django import forms
from django.core.mail import send_mail as sm
from django.db import models, transaction
from comovi.apps.core.translations import translations
from comovi.apps.core.models import InboxMessage, Property, User, get_path_user_profile_picture, AdminProfile, PropertyInterior
from django.views.generic import FormView
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from comovi.apps.core.models import *

class InboxMessageForm(forms.ModelForm):
    class Meta:
        model = InboxMessage
        fields = ('message',)
# class InboxMessageForm(forms.Form):
#     to = forms.CharField(required=True)
#     body = forms.Field(required=True)
#     subject = forms.CharField(required=True)

#     _to = []
#     _to_users = []
#     _body = ''
#     _subject = ''
#     _property = None

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request')
#         super(InboxMessageForm, self).__init__(*args, **kwargs)

#     def clean(self):
#         cleaned_data = super().clean()
#         self._subject = cleaned_data.get("subject", '')
#         self._body = cleaned_data.get("body", '')
#         to = cleaned_data.get('to', '')

#         if to.startswith('property-'):
#             to = to.replace('property-', '')
#             self._property = Property.objects.get(id=to)
#             admins = self._property.admin_profiles.all()
#             for admin in admins:
#                 self._to.append(admin.user.email)
#                 self._to_users.append(admin.user)
#         elif to.startswith('user-'):
#             to = to.replace('user-', '')
#             user = User.objects.get(id=to)
#             self._to.append(user.email)
#             self._to_users.append(user)

#         with transaction.atomic():
#             message = InboxMessage.objects.create(
#                 user=self.request.user,
#                 subject=self._subject,
#                 property=self._property,
#                 message=self._body
#             )
#             for user in self._to_users:
#                 message.to.add(user)
#             message.save()

#         return cleaned_data


class ProfileModelForm(forms.ModelForm):
    error_css_class = "form-errors"
    birth_date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'type':'date'
                                }))

    def __init__(self, *args, **kwargs):
        super(ProfileModelForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = _("Nombre de pila")
        self.fields['last_name'].label = _("Apellido")
        self.fields['mother_last_name'].label = _("Apellido de la madre")
        self.fields['gender'].label = _("Género")
        self.fields['birth_date'].label = _("Fecha de nacimiento")
        self.fields['phone'].label = _("Teléfonoo")
        self.fields['cell_phone'].label = _("Teléfono móvil")
        self.fields['profile_picture'].label = _("Foto de perfil")


    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mother_last_name',
            'rfc',
            'gender',
            'birth_date',
            'phone',
            'cell_phone',
            'profile_picture'
            )

    def clean_cell_phone(self):
        cell_phone = self.cleaned_data['cell_phone']
        if cell_phone:
            if len(cell_phone) < 8:
                raise ValidationError('Minimum 8 Numbers required')
        return cell_phone

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if len(phone) < 8:
                raise ValidationError('Minimum 8 Numbers required')
        return phone

    def clean_rfc(self):
        rfc = self.cleaned_data['rfc']
        if rfc:
            if len(rfc) < 10:
                raise ValidationError('Minimum 10 Character required')
        return rfc

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date:
            if birth_date >= birth_date.today():
                raise ValidationError('Birth date should not be greater than current date')
        return birth_date

class PropertyManagerForm(forms.ModelForm):
    password1 = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                    'type':'password',
                                    'autocomplete': 'off'
                                }))
    confirm_password = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                    'type':'password',
                                    'autocomplete': 'off'
                                }))

    def __init__(self, *args, **kwargs):
        super(PropertyManagerForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = _("Password")
        self.fields['confirm_password'].label = _("Confirm Password")
        self.fields['first_name'].label = _("Nombre de pila")
        self.fields['phone'].label = _("Teléfonoo")
        self.fields['profile_picture'].label = _("Foto de perfil")

    class Meta:
        model = User
        fields = ('first_name', 'phone', 'profile_picture')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if len(phone) < 8:
                raise ValidationError('Minimum 8 Numbers required')
        return phone

    def clean_confirm_password(self):
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['confirm_password']
        if p1 and p2:
            if p1 != p2:
                raise ValidationError(_("password did not match"))
        return p2


    def save(self, commit=True):
        m = super(PropertyManagerForm, self).save(commit=False)
        data = self.cleaned_data
        if data['password1'] and data['confirm_password']:
            m.set_password(data['confirm_password'])
        m.save()
        return m

class UserDisplayForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserDisplayForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = _("Nombre de pila")
        self.fields['last_name'].label = _("Apellido")
        self.fields['phone'].label = _("Teléfonoo")
        self.fields['profile_picture'].label = _("Foto de perfil")

    class Meta:
        model = User
        fields = ('first_name','last_name','email','phone','profile_picture')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'property', 'body', 'cover_image')

class PostAttachmentForm(forms.ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('file',)