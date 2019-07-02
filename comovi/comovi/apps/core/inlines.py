from django.contrib.admin import StackedInline, TabularInline

from comovi.apps.core.models import AddressProperty, ContactProperty, PropertyInterior, PropertyInteriorHasService, \
    PropertyPreferences, Payment, AdminProfile, OwnerProfile, PostAttachment


class AddressInline(StackedInline):
    model = AddressProperty
    extra = 0


class ContactInline(StackedInline):
    model = ContactProperty
    extra = 0


class PropertyInteriorInline(TabularInline):
    model = PropertyInterior
    extra = 0
    show_change_link = True
    show_full_result_count = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PropertyInteriorHasServiceInline(StackedInline):
    model = PropertyInteriorHasService
    extra = 0
    show_change_link = True


class PropertyPreferencesInline(StackedInline):
    model = PropertyPreferences
    extra = 1


class PaymentInline(StackedInline):
    model = Payment
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class AdminProfileInline(StackedInline):
    model = AdminProfile
    extra = 0
    fk_name = 'user'


class OwnerProfileInline(StackedInline):
    model = OwnerProfile
    extra = 0
    fk_name = 'user'


class PostAttachmentInline(StackedInline):
    model = PostAttachment
    extra = 0
