from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.utils import translation
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
from django.db.models import Q
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView, FormView
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from comovi.common.mail import MailManager
from comovi.apps.core.models import *
from comovi.apps.website.dashboard import Dashboard
from .translations import translations
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import UpdateView
from .forms import *
import uuid, io
import datetime, random, string
import json
from datetime import date , datetime
from django.utils.translation import gettext as _
now = datetime.now()
from django.contrib.auth import get_user_model
from comovi.sample import PayPalClient
from paypalcheckoutsdk.orders import OrdersGetRequest
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import pdb

# noinspection PyMethodMayBeStatic
class LoginView(TemplateView):
    template_name = 'website/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('website:index'))
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        UserModel = get_user_model()
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_uname = UserModel.objects.get(username=username)
        except Exception as e:
            user_uname = None
        try:
            user_email = UserModel.objects.get(email=username)
        except Exception as e:
            user_email = None
        if user_uname:
            if user_uname.is_active:
                if user_uname.check_password(password):
                    login(request, user_uname)
                    return redirect(reverse('website:index'))
                else:
                    error = _('Incorrect Password')
            else:
                error = translations['inactive_user']
        elif user_email:
            if user_email.is_active:
                if user_email.check_password(password):
                    login(request, user_email)
                    return redirect(reverse('website:index'))
                else:
                    error = _('Incorrect Password')
            else:
                error = translations['inactive_user']
        else:
            user_exist = User.objects.filter(username=username).count() > 0
            language = translation.get_language_from_request(request)
            error = _('Incorrect Password') if user_exist else _('User does not exist')
        return TemplateResponse(template=self.template_name, request=request, context={'error': error})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'website/dashboard_2.html' # changes index to dashboard.html


class PageView(LoginRequiredMixin, TemplateView):
    template_name = 'website/real-cerezos.html'


# class InboxView(LoginRequiredMixin, ListView):
#     template_name = 'website/inbox.html'
#     model = InboxMessage
#     context_object_name = 'messages'
#     paginate_by = 15
#     #queryset = InboxMessage.objects.all().order_by('-date_creation')

#     def get_queryset(self):
#         queryset = super(InboxView, self).get_queryset()
#         if hasattr(self.request.user, 'admin_profile') and self.request.user.admin_profile:
#             return InboxMessage.objects.filter(Q(to__id__in=[self.request.user.id]) |
#                                    Q(property__id__in=self.request.user.admin_profile.my_properties().values_list('id',
#                                                                                                                   flat=True))).order_by(
#                 '-date_creation')
#         elif hasattr(self.request.user, 'owner_profile') and self.request.user.owner_profile:
#             return InboxMessage.objects.filter(to__id__in=[self.request.user.id],
#                                    property__id__in=self.request.user.owner_profile.my_properties().values_list('id',
#                                                                                                                   flat=True)).order_by('-date_creation')
#         else:
#             return InboxMessage.objects.filter(to__id__in=[self.request.user.id]).order_by('-date_creation')

class InboxView(LoginRequiredMixin, ListView):
    template_name = 'website/inbox.html'
    model = Conversation
    context_object_name = 'convs'
    paginate_by = 15
    queryset = Conversation.objects.all().order_by('-date_creation','-date_modification')

    def get_queryset(self, *args, **kwargs):
        queryset = super(InboxView, self).get_queryset(*args, **kwargs)
        if hasattr(self.request.user, 'admin_profile') and self.request.user.admin_profile:
            return queryset.filter(user=self.request.user.id).order_by('-date_creation','-date_modification').distinct()
        elif hasattr(self.request.user, 'owner_profile') and self.request.user.owner_profile:
            return queryset.filter(receivers__id__in=[self.request.user.id]).order_by('-date_creation','-date_modification').distinct()    
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super(InboxView, self).get_context_data(**kwargs)
        context['un_seen'] = MessageMeta.objects.filter(is_seen=False, user_id=self.request.user.id).select_related('message')
        context['delete'] = InboxMessage.objects.filter(user__id=self.request.user.id)
        return context

class ConverstaionView(LoginRequiredMixin, View):
    form_class = InboxMessageForm
    template_name = 'website/conversation.html'

    def get(self, request, conv_id, *args, **kwargs):
        form = self.form_class()
        conv = get_object_or_404(Conversation, id=conv_id)
        return render(request, self.template_name, {'form' : form, 'conversation' : conv})

    def post(self, request, conv_id, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            conv = get_object_or_404(Conversation, id=conv_id)
            message.conversation = conv
            message.save()
            MessageMeta.objects.get_or_create(user=conv.user, message=message, is_seen=True if request.user == conv.user else False)
            for receiver in conv.receivers.all():
                MessageMeta.objects.get_or_create(user=receiver, message=message, is_seen=True if request.user == receiver else False)
            return render(request, self.template_name, {'form' : self.form_class(), 'conversation' : conv})
        return render(request, self.template_name, {'form' : form, 'conversation' : conv})


@login_required
def SeenMsgs(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        if data.get('id'):
            obj = get_object_or_404(Conversation, id=data["id"])
            
            if request.user == obj.user:
                for i in obj.messages.select_related():
                    for j in i.metas.select_related():
                        if request.user == j.user:
                            if j.is_seen == False:
                                j.is_seen = True
                                i = j
                                obj = i
                                obj.save()
            else:
                for i in obj.receivers.select_related():
                    for j in i.message_metas.select_related():
                        if j.is_seen == False:
                            j.is_seen = True
                            i = j
                            obj = i
                            obj.save()           

            return JsonResponse({"success": True})
        else:
            return JsonResponse(status=403, data={"success": False, "error": "dont get data"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})


@login_required
def Deletemsg(request):
    if request.method =='POST':
        data = request.POST.getlist('id[]')
        if data:
            for i in data:
                obj = get_object_or_404(Conversation, id=i)
                obj.delete()
            return JsonResponse(status=200, data={"success": True, "message": "Delete message Successfully"})
        else:
            return JsonResponse(status=403, data={"success": False, "error": "dont get data"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})
    


class InboxDetailView(LoginRequiredMixin, DetailView):
    template_name = 'website/inbox_detail.html'
    model = InboxMessage

    def get_context_data(self, **kwargs):
        context = super(InboxDetailView, self).get_context_data(**kwargs)
        context['id'] = self.get_object().id
        return context


class SendEmailView(LoginRequiredMixin, FormView):
    template_name = 'website/send_email.html'
    model = InboxMessage
    form_class = InboxMessageForm
    success_url = '/inbox/sent/'

    def get_form_kwargs(self):
        kwargs = super(SendEmailView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class SentInboxView(InboxView):

    def get_queryset(self):
        return self.request.user.sent_messages.all().order_by('-date_creation')


class PaymentInteriorView(LoginRequiredMixin, ListView):
    template_name = 'website/payments.html'
    model = PropertyInteriorHasService
    context_object_name = "payments"
    paginate_by = 15
    # queryset = PropertyInteriorHasService.objects.all() \
    #     .select_related('property_interior') \
    #     .select_related('service')

    def get_queryset(self):
        queryset = PropertyInteriorHasService.objects.filter(property_interior__resident=self.request.user)
        user = self.request.user
        is_root = user.is_superuser
        is_admin = False if not hasattr(user, 'admin_profile') or not user.admin_profile else True
        is_owner = False if not hasattr(user, 'owner_profile') or not user.owner_profile else True
        # queryset = super(PaymentInteriorView, self).get_queryset()
        if is_root:
            return queryset
        if is_admin:
            properties = user.admin_profile.properties_managed.through.objects.all().values('property_id')
            return queryset.filter(property_interior__property__id__in=properties)
        if is_owner:
            property_interiors = user.owner_profile.property_interiors_owned.through.objects.all().values(
                'propertyinterior_id')
            return queryset.filter(property_interior__id__in=property_interiors)
        return PropertyInteriorHasService.objects.none()


class PaymentView(LoginRequiredMixin, ListView):
    template_name = 'website/history.html'
    model = Payment
    context_object_name = 'payments'
    paginate_by = 30
    queryset = Payment.objects.all().order_by('-payment_datetime')

    def get_queryset(self):
        user = self.request.user
        is_root = user.is_superuser
        is_admin = False if not hasattr(user, 'admin_profile') or not user.admin_profile else True
        is_owner = False if not hasattr(user, 'owner_profile') or not user.owner_profile else True
        queryset = super(PaymentView, self).get_queryset()
        if is_root:
            return queryset
        if is_admin:
            properties = user.admin_profile.properties_managed.through.objects.all().values('property_id')
            return queryset.filter(property_interior_has_service__property_interior__property_id__in=properties)
        if is_owner:
            property_interiors = user.owner_profile.property_interiors_owned.through.objects.all().values(
                'propertyinterior_id')
            return queryset.filter(property_interior_has_service__property_interior__id__in=property_interiors)
        return PropertyInteriorHasService.objects.none()


class NewspaperView(LoginRequiredMixin, ListView):
    template_name = 'website/newspaper.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 30
    queryset = Post.objects.all().select_related('category').order_by('-date_creation')

    def get_queryset(self):
        user = self.request.user
        is_owner = False if not hasattr(user, 'owner_profile') or not user.owner_profile else True
        queryset = super(NewspaperView, self).get_queryset()
        queryset = self.filter_params(queryset)
        if is_owner:
            return queryset.filter(is_active=True)
        return queryset

    def filter_params(self, queryset):
        category = self.request.GET.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        _property = self.request.GET.get('property', None)
        if _property and _property != '':
            queryset = queryset.filter(property_id=_property)
        elif hasattr(self.request.user, 'owner_profile') and self.request.user.owner_profile:
            properties = self.request.user.owner_profile.my_properties().values_list('id', flat=True)
            queryset = queryset.filter(property__id__in=properties)
        elif hasattr(self.request.user, 'admin_profile') and self.request.user.admin_profile:
            properties = self.request.user.admin_profile.my_properties().values_list('id', flat=True)
            queryset = queryset.filter(property__id__in=properties)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(NewspaperView, self).get_context_data(**kwargs)
        try:
            context['property'] = self.request.user.admin_profile.my_properties()
        except:
            pass
        context['category'] = PostCategory.objects.all()

        return context

@login_required
def SeenNews(request):
    if request.method == "POST":
        data = request.POST
        try:
            obj = get_object_or_404(Post, id=data['id'])
            obj.seen = True
            obj.save()

        except Exception as e:
            return JsonResponse({"status": False})

        return JsonResponse({"success": True})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})

# noinspection PyMethodMayBeStatic
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('website:login'))


class PropertyView(LoginRequiredMixin, DetailView):
    template_name = 'website/property.html'
    model = Property

    def get_context_data(self, **kwargs):
        obj = kwargs['object']

        preferences = obj.make_preferences()
        kwargs.update({
            'preferences': preferences,
            'property_interiors_stat': Dashboard.make_property_interiors_stat(obj),
            'service_stats': Dashboard.make_services_to_show(preferences.services_to_show.all())
        })

        return super(PropertyView, self).get_context_data(**kwargs)


class PropertyInteriorView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = 'website/property_interior.html'
    model = PropertyInterior
    queryset = PropertyInterior.objects.all()
    success_message = _("Profile Successfully Updated")

    def get_context_data(self, **kwargs):
        return super(PropertyInteriorView, self).get_context_data(**kwargs)


class PayView(LoginRequiredMixin, DetailView):
    template_name = 'website/pay.html'
    model = PropertyInteriorHasService
    # queryset = PropertyInteriorHasService.objects.all()



class EditUserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView): 
    template_name = "website/my_profile.html"
    form_class = ProfileModelForm
    success_message = "Profile Successfully Updated"
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = now.strftime("%m/%d/%Y")
        return context


def LanguageSelect(request):
    if request.method == "POST":
        user_language = request.POST['language']
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        next = request.POST.get('next', '/')
        print(next)
        if len(next) > 3:
            next = next[3:]
        print(next)
        return HttpResponseRedirect(next)

class ProperyManagerView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'website/property_manager.html'
    form_class = PropertyManagerForm
    success_message = ("Profile Successfully Updated")
    success_url = '/property-manager'

    def get_object(self, queryset=None):
        return self.request.user

class PropertyManageInteriors(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = 'website/property_manage_inetriors_details.html'
    model = Property
 
    def get_context_data(self, **kwargs):
        context = super(PropertyManageInteriors, self).get_context_data(**kwargs)
        context['property_id'] = self.get_object().id
        return context

class CondiniumUserManage(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = 'website/condinum_user.html'
    model = Property

    def get_context_data(self, **kwargs):
        context = super(CondiniumUserManage, self).get_context_data(**kwargs)
        context['property_id'] = self.get_object().id
        context['available_interiors'] = context['object'].interiors.select_related().filter(resident=None)
        return context

@login_required
def CreateUserWithResident(request):
    if request.method == "POST":
        data = request.POST
        if data.get('first_name') and data.get('last_name') and data.get('email') and data.get('interior_id'):
            print('in if')
            if User.objects.filter(username=data.get('email')):
                return JsonResponse(status=403, data={"success": False, "error": "Already User Exists"})
           
            u = User(first_name=data['first_name'], last_name=data['last_name'], \
            email=data['email'], username=data['email'])
            char_set = string.ascii_uppercase + string.digits
            pwd = ''.join(random.sample(char_set*16, 8))
            u.set_password(pwd)
            u.created_by = request.user
            u.save()
            i = PropertyInterior.objects.get(id=data['interior_id'])
            i.resident = u
            i.status_occupancy = 2
            i.save()
            owner = OwnerProfile(user=u)
            owner.save()
            manager = MailManager()

            try:
                data = CommonEmailTemplate.objects.filter(name_of_template='new_condominium_user.html')
            except Exception as e:
                print(e)
                return JsonResponse({"status": False})

            for x in data:
                content = x.content

            manager.send_new_condonium_user(u.email, '{} {}'.format(u.first_name, u.last_name),
                i.property.name, pwd, content, request.build_absolute_uri(reverse('website:login')))
            return JsonResponse(status=200, data={"success": True, "message": "Condominium User Created"})
        else:
            return JsonResponse(status=403, data={"success": False, "error": "dont get data"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})


@login_required
def UpdateUserById(request):
    print("in update user")
    if request.method == 'POST':
        data = request.POST
        p = PropertyInterior.objects.get(property__id=request.POST.get('property_id'), resident__id=request.POST.get('id'))
        user = p.resident
        if data['first_name']:
            user.first_name = data["first_name"]
        if data['last_name']:
            user.last_name = data["last_name"]
        if data['email']:
            user.email = data["email"]
        if data['interior_id']:
            p.number = data['interior_id']
        p.status_occupancy = 2
        p.save()
        user.save()
        return JsonResponse(status=200, data={"status": True, "message": "Condominium User Successfully Updated"})
    else:
        return JsonResponse(status=404, data={"status": "Page Not Found"})

@login_required
def DeleteUserById(request):
    if request.method == "POST":
        print("data delete", request.POST)
        p = PropertyInterior.objects.get(property__id=request.POST.get('property_id'), resident__id=request.POST.get('user_id'))
        user = p.resident
        p.resident = None
        p.status_occupancy = 1
        p.save()
        user.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse(status=404, data={"status": "Page Not Found"})

class PropertyDashboard(LoginRequiredMixin, DetailView):
    template_name = 'website/property_dashboard.html'
    model = Property

    def get_context_data(self, **kwargs):
        context = super(PropertyDashboard, self).get_context_data(**kwargs)
        interiors = context['object'].interiors.select_related()
        print(interiors)
        count =1
        context['number']  = len(interiors)
        print(context['number'])
        total_amt = 0
        paid_amt = 0
        for inter in interiors:
            total_amt += inter.getTotalAmount()
            paid_amt += inter.getPaidAmount()
        context['unpaid_amount'] = total_amt - paid_amt
        context['paid_amount'] = paid_amt
        if total_amt > 0:
            context['percentage_paid'] = int(paid_amt/total_amt * 100)
            context['percentage_unpaid'] = int((total_amt-paid_amt)/total_amt * 100)

        return context

@login_required
def CreateNewInterior(request):
    if request.method == "POST":
        data = request.POST
        if data.get('property_id') and data.get('interior_number') and len(data.get('interior_number')) in range(1,51):
            pi = PropertyInterior.objects.filter(property__id=data['property_id'], number=data['interior_number'])
            if pi:
                return HttpResponse(json.dumps({'status': False, "message": "Interior number Already exist"}), content_type="application/json")
            try:
                pi = PropertyInterior(number=data['interior_number'], property_id=data['property_id'])
                pi.save()
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({'status': e}), content_type="application/json")
            return HttpResponse(json.dumps({'status': True, "message": "Interior Created Successfully"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': False}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': False}), content_type="application/json")

@login_required
def EditNewInterior(request):
    if request.method == "POST":
        data = request.POST
        if data['interior_number'] and data['Property_id'] and data['Interior_id']:
            if PropertyInterior.objects.filter(number=data['interior_number'], property__id=data['Property_id']):
                return JsonResponse(status=403, data={"success": False, "error": "Interior Number Updated Successfully"})
            else:
                pi = PropertyInterior.objects.get(id=data['Interior_id'])
                pi.number = data['interior_number']
                pi.save()
                return JsonResponse(status=200, data={"success": True, "message": "Interior Number Updated Successfully"})
        else:
            return JsonResponse(status=403, data={"error": "there was an error"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})



class InteriorDetail(LoginRequiredMixin, UpdateView):
    model = PropertyInterior
    fields = ('number', 'resident')
    template_name = "website/interior_detail.html"

    def get_context_data(self, **kwargs):
        context = super(InteriorDetail, self).get_context_data(**kwargs)
        context['interior_services'] = PropertyInteriorHasService.objects.filter(property_interior=self.object.id)
        context['paymenttype'] = PaymentType.objects.all()
        context['periodic'] = CatalogService.PERIODICITY_CHOICES
        context['catalog'] = CatalogService.objects.all()
        context['payment_status'] = PropertyInteriorHasService.SERVICE_STATUS_CHOICES
        return context

@login_required
def DeleteNewInterior(request):
    if request.method == "POST":
        data = request.POST
        if data['interior_id']:
            obj = get_object_or_404(PropertyInterior, id=data['interior_id'])           
            obj.delete()
            return JsonResponse({"success": True, "message": "Delete Interior Successfully"})
        else:
            return JsonResponse(status=404, data={"error": "Page Not Found"})
        

class UserDisplay(LoginRequiredMixin, UpdateView):
    template_name = "website/user_display.html"
    model = PropertyInterior
    fields = '__all__'


class PropertyManagerCondonium(LoginRequiredMixin, UpdateView):
    template_name = "website/property_manager_condonium_profile.html"
    model = PropertyInterior
    fields = '__all__'


class HistoricDisplay(LoginRequiredMixin, DetailView):
    template_name = 'website/condinium_template.html'
    model = Property

    def get_context_data(self, **kwargs):
        context = super(HistoricDisplay, self).get_context_data(**kwargs)
        context['property_id'] = self.get_object().id
        context['data'] =  context['property'].interiors.select_related()
        return context

class InteriorUserDisplay(LoginRequiredMixin, UpdateView):
    template_name = "website/interior_user_profile.html"
    model = PropertyInterior
    fields = '__all__'


class InteriorHistoricDisplay(LoginRequiredMixin, DetailView):
    template_name = 'website/interior_condonium_user.html'
    model = Property

    def get_context_data(self, **kwargs):
        context = super(InteriorHistoricDisplay, self).get_context_data(**kwargs)
        context['property_id'] = self.get_object().id
        context['data'] =  context['property'].interiors.select_related()
        return context


@login_required
def CreateNotice(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'error' : False, 'message' : "Notice uploaded successfully"})
        else:
            return JsonResponse({'error' : True, 'errors' : form.errors, 'message' : "Please Fill All Details"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})


@login_required
def DeleteNotice(request):
    if request.method == 'POST':
        data =  request.POST
        if not request.POST.get('category_id'):
            return JsonResponse(status=403, data={"status":False, "error": "id not Found"})
        P = Post.objects.get(pk=data["category_id"])
        P.delete()
        return JsonResponse({"success": True, 'message' : "Notice Deleted Successfully"})

    else:
        return JsonResponse(status=404, data={"status": "Page Not Found"})

@login_required
def SaveEditNotice(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(Post, id=id)
        form = PostForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return JsonResponse({'error' : False, 'message' : "Edit Notice successfully"})
        else:
            return JsonResponse({'error' : True, 'errors' : form.errors})
    else:
        return JsonResponse(status=404, data={"status": "Page Not Found"})

@login_required
def EditNotice(request):
    if request.method == 'POST':
        data = request.POST 
        a =  Post.objects.get(id=data['id'])
        print(a)
        if data['update'] == "ok":
            a.title = data['title']
            a.category_id = data['category_id']
            a.property_id = data['property_id']
            a.body = data['body']
            a.cover_image =data['cover_image']
            a.save()
        try:
            c_img = a.cover_image.url
            
        except:
            c_img = None
        d = {
            'title' : a.title,
            'category_id' : str(a.category.id),
            'property_id' : str(a.property.id),
            'body' : a.body,
            'cover_image' : c_img,
        }
        
    return HttpResponse(json.dumps({'status': True, "message": "Edit Notice Successfully", "data" : d}), content_type="application/json")


@login_required
def getInteriorServiceDetail(request):
    if request.method == "POST":
        data = request.POST
        if data.get('service_id'):
            obj = get_object_or_404(PropertyInteriorHasService, pk=data["service_id"])
            return JsonResponse({"amount": obj.amount, "service": obj.service.periodicity, "id": obj.id, \
                "duedate": obj.due_date, "status_payment": obj.status_payment})
        return JsonResponse(status=403, data={"error": "bad request"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})

@login_required
def updateInteriorService(request):
    if request.method == "POST":
        data = request.POST
        if data.get('service_id') and data.get('updatedamount') and data.get('periodic') and \
        data.get('paymentstatus') and data.get('duedate'):
            obj = get_object_or_404(PropertyInteriorHasService, pk=data["service_id"])
            obj.amount = data["updatedamount"]
            obj.due_date = data["duedate"]
            obj.status_payment = data["paymentstatus"]
            srv = obj.service
            srv.periodicity = int(data["periodic"])
            srv.save()
            obj.service = srv
            obj.save()
            return JsonResponse({"success": True, "message": "Interior Service Updated Successfully"})
        return JsonResponse(status=403, data={"error": "bad request"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})

@login_required
def deleteInteriorService(request):
    if request.method == "POST":
        data = request.POST
        if data.get('service_id'):
            obj = get_object_or_404(PropertyInteriorHasService, pk=data["service_id"])
            obj.delete()
            return JsonResponse({"success": True, "message": "Interior Service Updated Successfully"})
        return JsonResponse(status=403, data={"error": "bad request"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})


@login_required
def createInteriorService(request):
    if request.method == "POST":
        data = request.POST
        if data.get('Interior_id') and data.get('amount') and data.get('duedate') and \
        data.get('payment_status') and data.get('Periodicity') and data.get('catalog'):
            interior = get_object_or_404(PropertyInterior, pk=data['Interior_id'])
            cat = get_object_or_404(CatalogService, pk=data["catalog"])
            inhasservice = PropertyInteriorHasService(property_interior=interior,service=cat, \
                amount=data["amount"], due_date=data["duedate"], status_payment=data["payment_status"])
            inhasservice.save()
            return JsonResponse({"success": True, "message": "Interior Service Added Successfully"})
        return JsonResponse(status=403, data={"error": "bad request"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})

@login_required
def updateDate(request):
    if request.method == "POST":
        data = request.POST
        if data.get('id') and data.get('modifydate'):
            obj = get_object_or_404(PropertyInterior, pk=data["id"])
            obj.date_modification = data['modifydate']
            obj.status_occupancy = 1
            obj.resident = None
            obj.save()
            return JsonResponse({"success": True, "message": "Condominium User Moved Out Successfully"})
        return JsonResponse(status=403, data={"error": "bad request"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})

class GetOrder(PayPalClient):  
    def get_order(self, order_id):
        request = OrdersGetRequest(order_id)
        response = self.client.execute(request)
        print("response is ", response)
        print('Status Code: ', response.status_code)
        print('Status: ', response.result.status)
        print('Order ID: ', response.result.id)
        print('Intent: ', response.result.intent)
        print('Links:')
        for link in response.result.links:
          print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
        print('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                           response.result.purchase_units[0].amount.value))

from django.core.files import File


@login_required
@csrf_exempt
def GetData(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            ps = PropertyInteriorHasService.objects.get(pk=body["serviceID"])
            oid = body['orderID']
            GetOrder().get_order(oid)
        except Exception as e:
            print(e)
            return JsonResponse({"status": False})
        else:
            with transaction.atomic():
                buffer = io.BytesIO()
                p = canvas.Canvas(buffer)
                st = "Payment Invoice Service - {} Amount - {} Order ID - ".format(ps.service.name, ps.amount, oid)
                p.drawString(100,750,st)
                p.showPage()
                p.save()

                ps.invoice.save("invoice.pdf", buffer)

                ps.status_payment = 3
                print("pdf is ", ps.invoice)
                ps.save()
                p = Payment(property_interior_has_service=ps, approval_number=body["serviceID"], \
                    payment_datetime=timezone.now())
                p.save()
                return JsonResponse({"status": True})

from django.template.loader import render_to_string

@login_required
def Tmpp(request):
    context = {
        "object":[
        {"title": "Lorem Ipsum is simply dummy text",
        "desc": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout.",
        "amount": 40.00,
        "qty": 1,
        "total": 40.00}
        ],
        "gtotal": 40.00,
        "orderID": 2321312,
    }
    return render(request, "website/tmp.html", context)                

def password_reset(request):
    if request.method == 'POST':
        data = request.POST
        user_email = data.get('email')
        try:
            user = User.objects.get(email=user_email)
        except Exception as e:
            print(str(e))
            return JsonResponse(status=400, data={'error' : 'Please try again with the email address that was used for registration'})
        try:
            char_set = string.ascii_uppercase + string.digits
            random_pass = ''.join(random.sample(char_set*16, 8))
            user.set_password(random_pass)
            mail_manager = MailManager()
            try:
                data = CommonEmailTemplate.objects.filter(name_of_template='forget_password.html')
            except Exception as e:
                print(e)
                return JsonResponse({"status": False})

            for x in data:
                content = x.content
       
            mail_manager.send_forgot_password(user.email, '{} {}'.format(user.first_name, user.last_name), random_pass, content, request.build_absolute_uri(reverse('website:login')))
            user.save()
        except Exception as e:
            return JsonResponse(status=400, data={'error' : str(e)})
        return JsonResponse(status=200, data={"success": True, "message": "You have successfully send password to registered user email id!"})
    else:
        return JsonResponse(status=404, data={"error": "Page Not Found"})



@csrf_exempt
@login_required
def add_post_attachment(request, post_id):
    if request.method == 'POST':
        try:
            post = get_object_or_404(Post, id=post_id)
        except Exception as e:
            return JsonResponse(status=400, data={'error' : 'Invalid notice id'})
        form = PostAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            post_attachment = form.save(commit=False)
            post_attachment.post = post
            post_attachment.save()
            return JsonResponse(status=200, data={'is_valid' : True, 'name' : post_attachment.file.name, 'url' : post_attachment.file.url})
        else:
            return JsonResponse(status=400, data={'is_valid' : False})
    else:
        return JsonResponse(status=404, data={'error' : 'Page not found'})



class EmailView(TemplateView):
    template_name='website/send_email.html'

