from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin, csrf_protect_m
from django.shortcuts import redirect
from django.urls import reverse

from comovi.apps.core.inlines import *
from comovi.apps.core.translations import translations
from comovi.apps.core.models import *


# noinspection PyUnresolvedReferences
class BasePreferencesAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        if not issubclass(self.model, PreferenceMixin):
            raise Exception('Preference object must inherit PreferenceMixin')
        obj = self.model.get()
        return redirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name),
                                args=(obj.id,)))


@admin.register(User)
class PlatformUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        (translations['permissions'], {'fields': ('is_active', 'is_staff',)}),
        (translations['personal_data'], {'fields': ('first_name', 'last_name', 'mother_last_name',
                                                    'rfc', 'birth_date', 'gender', 'profile_picture',)}),
    )

    inlines = [
        AdminProfileInline,
        OwnerProfileInline,
    ]

    list_display = ('username', 'first_name', 'last_name', 'mother_last_name', 'is_active')
    list_filter = ('is_active',)

    search_fields = ('username', 'first_name', 'last_name', 'mother_last_name', 'email',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
        ContactInline,
        PropertyInteriorInline,
        PropertyPreferencesInline
    ]


@admin.register(PropertyInterior)
class PropertyInteriorAdmin(admin.ModelAdmin):
    inlines = [
        PropertyInteriorHasServiceInline
    ]


@admin.register(PropertyInteriorHasService)
class PropertyInteriorHasService(admin.ModelAdmin):
    inlines = [
        PaymentInline
    ]


@admin.register(ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(SitePreferences)
class SitePreferencesAdmin(BasePreferencesAdmin):
    pass


@admin.register(CatalogService)
class CatalogServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    pass

@admin.register(InboxMessage)
class InboxMessageAdmin(admin.ModelAdmin):
   pass

@admin.register(MessageMeta)
class MessageMetaAdmin(admin.ModelAdmin):
    pass


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        PostAttachmentInline
    ]


@admin.register(PostAttachment)
class PostAttachmentAdmin(admin.ModelAdmin):
    pass

@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Payment)
class PaymentTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(CommonEmailTemplate)
class CommonEmailTemplateAdmin(admin.ModelAdmin):
    pass

@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    pass

