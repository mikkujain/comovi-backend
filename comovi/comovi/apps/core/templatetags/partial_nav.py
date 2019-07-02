# from django import template
# from comovi.apps.core.models import InboxMessage
# from django.db.models import Q
# register = template.Library()

# def unraed_messages(self):
# 	if hasattr(self.request.user, 'admin_profile'):
# 		return InboxMessage.objects.filter(Q(to__id__in=[self.request.user.id]) |Q(property__id__in=self.request.user.admin_profile.my_properties().values_list('id', flat=True))).filter(is_seen=False).count
# 	elif hasattr(self.request.user, 'owner_profile'):
# 		return InboxMessage.objects.filter(to__id__in=[self.request.user.id],property__id__in=self.request.user.owner_profile.my_properties().values_list('id',flat=True)).filter(is_seen=False).count
# 	else:
# 		return InboxMessage.objects.filter(to__id__in=[self.request.user.id]).order_by('-date_creation')
		
# register.simple_tag(unraed_messages)
