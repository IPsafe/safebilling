# -*- coding: utf-8 -*-

from ipsafe.core.models import *
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from forms import *
from django.forms import MultipleChoiceField
from ipsafe.freeswitch.parser import parse_devices, parse_providers
from datetime import timedelta

class BlacklistAdmin(admin.ModelAdmin):
    list_display = ('did', 'description')
    list_filter = ('did', 'description')
    search_fields = ['did', 'description']
    fields = ('did', 'description')

    def save_model(self, request, obj, form, change):
        obj.user = request.user        
        #obj.customer = get_customer_by_user(request.user.id)
        obj.save()


class DevicesAdmin(admin.ModelAdmin):
    form = DeviceForm
    readonly_fields = ('id',)
    classes = ('collapse closed',)

    fieldsets = (
        ('', {
            'fields': ['customer', 'name', 'password', 'description', ('callerid', 'callerid_number'), 'dialrules_groups', ('host', 'port'), ],
        }),
        (u'Mais configurações', {
            'classes': ('collapse closed',),
            'fields': ('codec_inbound', 'codec_outbound', 'bypass_media'),
        }),                 
    )
  
    list_display = ('name', 'customer', 'host', 'callerid','dialrules_groups',)
    list_filter = ('name', 'customer', 'host','callerid','dialrules_groups',)
    search_fields = ['name', 'host', 'callerid',]

    class Media:
        js = ['/static/admin/js/hide_fields.js',]


    def save_model(self, request, obj, form, change):
        #if not request.user.is_superuser:
        #    obj.user = request.user
        #obj.customer = get_customer_by_user(request.user.id)
        if 'customer' in request.GET:
            obj.customer_id = request.GET['customer']
        obj.save()
        parse_devices(None)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = {}
        if 'customer' in request.GET:
            extra_context['set_button_url'] = 'add/?customer=%s' % request.GET['customer']
        return super(DevicesAdmin, self).changelist_view(request, extra_context=extra_context)

    def add_view(self, request, extra_context=None):
        extra_context = {}
        if 'customer' in request.GET:
            extra_context['set_button_url'] = 'add/?customer=%s' % request.GET['customer']
        if 'customer' in request.POST:
            extra_context['set_button_url'] = 'add/?customer=%s' % request.POST['customer']
        return super(DevicesAdmin, self).add_view(request, extra_context=extra_context)

    def response_add(self, request, obj, post_url_continue="../%s/"):
        if not '_continue' in request.POST:
            if 'customer' in request.GET:
                post_url_continue = '/core/device/?customer=%s' % request.GET['customer']
            if 'customer' in request.POST:
                post_url_continue = '/core/device/?customer=%s' % request.POST['customer']
            return HttpResponseRedirect(post_url_continue)
        else:
            return super(DevicesAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        get_other_app_url = ''
        if not '_continue' in request.POST:
            if 'customer' in request.GET:
                get_other_app_url = '/core/device/add/?customer=%s' % request.GET['customer']
            if 'customer' in request.POST:
                get_other_app_url = '/core/device/add/?customer=%s' % request.POST['customer']
            return HttpResponseRedirect(get_other_app_url)
        else:
            return super(DevicesAdmin, self).response_change(request, obj)


class ProviderRulesInline(admin.TabularInline):
    model = ProviderRule    
    form = ProviderRulesForm    
    extra = 1

class GatewaysAdmin(admin.ModelAdmin):
    preserve_filters = True
    form = GatewaysForm
    model = Gateway
    inlines = [ProviderRulesInline,]
    readonly_fields = ('id',)
    classes = ('collapse closed',)

    fieldsets = (
        ('', {
            'fields': ['provider', 'description','password', ('callerid', 'callerid_number'), ('host', 'port'), 'register', ('fromuser', 'fromdomain',), 'codec_inbound', 'codec_outbound',],
        }),
    )
  
    list_display = ('description','provider', 'host','callerid',)
    list_filter = ('description','provider', 'host','callerid',)
    search_fields = ['description','host','callerid',]

    def save_model(self, request, obj, form, change):
        if 'provider' in request.GET:
            obj.provider_id = request.GET['provider']

        obj.save()
        parse_providers(None)

    class Media:
        js = ['/static/admin/js/template.gateway.js']

    def changelist_view(self, request, extra_context=None):
        extra_context = {}
        if 'provider' in request.GET:
            extra_context['set_button_url'] = 'add/?provider=%s' % request.GET['provider']

        return super(GatewaysAdmin, self).changelist_view(request, extra_context=extra_context)

    def add_view(self, request, extra_context=None):
        extra_context = {}
        if 'provider' in request.GET:
            extra_context['set_button_url'] = 'add/?provider=%s' % request.GET['provider']
        if 'provider' in request.POST:
            extra_context['set_button_url'] = 'add/?provider=%s' % request.POST['provider']

        return super(GatewaysAdmin, self).add_view(request, extra_context=extra_context)

    def response_add(self, request, obj, post_url_continue="../%s/"):
        if not '_continue' in request.POST:
            if 'provider' in request.GET:
                post_url_continue = '/core/gateway/?provider=%s' % request.GET['provider']
            if 'provider' in request.POST:
                post_url_continue = '/core/gateway/?provider=%s' % request.POST['provider']
            return HttpResponseRedirect(post_url_continue)
        else:
            return super(GatewaysAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        get_other_app_url = ''
        if not '_continue' in request.POST:
            if 'provider' in request.GET:
                get_other_app_url = '/core/gateway/add/?provider=%s' % request.GET['provider']
            if 'provider' in request.POST:
                get_other_app_url = '/core/gateway/add/?provider=%s' % request.POST['provider']
            return HttpResponseRedirect(get_other_app_url)
        else:
            return super(GatewaysAdmin, self).response_change(request, obj)

class ProvidersAdmin(admin.ModelAdmin):
    model = Provider
    form = ProviderForm
    exclude = ('context',)
    list_display = ['name', 'postpaid_limit', 'rate_group', 'gateway']
    fieldsets = (
        ('', {
            'fields': ['name', 'email', 'address', 'phone_number', 'web_site', 'postpaid_limit', 'rate_group', ],
        }),
    )

    def gateway(self,obj): # Implementar filtros de devices por usuário
        return u'''
                <a href="/core/gateway/add/?provider=%s" class="btn btn-small">
                    <i class="btn-icon-only icon-plus"></i>Adicionar
                </a>

                <br/>

                <a href="/core/gateway/?provider=%s" class="btn btn-small">
                    <i class="btn-icon-only icon-search"></i>Listar
                </a>

            ''' % (obj.id, obj.id)

    gateway.allow_tags = True
    gateway.short_description = 'Gateways'

    def save_model(self, request, obj, form, change):
        obj.save()
        parse_providers(None)

class LcrProvidersAdmin(admin.TabularInline):
    model = LcrProvider
    form = LcrProviderForm
    sortable_field_name = 'priority'
    sortable_order_field = 'priority'    
    #exclude = ('priority',)

    class Media:
        css = {
            'all': ('admin/css/admin-inlines.css', )
        }

class LcrAdmin(admin.ModelAdmin):
    inlines = [LcrProvidersAdmin,]
    readonly_fields = ('id',)
    #exclude = ('user',)
    list_display = ('name', 'order')
    list_filter = ('name', 'order')
    search_fields = ['name', 'order']
    fields = ('name', 'order')

    def save_model(self, request, obj, form, change):
        obj.user = request.user        
        #obj.customer = get_customer_by_user(request.user.id)
        obj.save()

class DialrulesAdmin(admin.TabularInline):
    model = Dialrule
    form = DialrulesForm

class DialrulesGroupsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_filter = ['name']
    search_fields = ['name']
    list_display = ['name']
    inlines = [DialrulesAdmin,]
    fields = ['name',]

    def save_model(self, request, obj, form, change):
        obj.user = request.user        
        #obj.customer = get_customer_by_user(request.user.id)
        obj.save()

    def queryset(self, request):
        qs = super(DialrulesGroupsAdmin, self).queryset(request)
        if not request.user.is_superuser:            
            #return qs.filter(customer=get_customer_by_user(request.user.id)) # Manter para implementacao de revendas
            return qs.filter(user=request.user.id)
        return qs
                
class RateTagsAdmin(admin.ModelAdmin):
    model = RateTag

class RatesAdmin(admin.StackedInline):
    form = RatesForm
    model = Rate
    exclude = ('tags_string',)
    fields = ('tag', 'prefix', ('min_time', 'increment'), 'price', 'gateway')
    extra = 1

    class Media:
        js = ['/static/admin/js/template.rate.js',]

class RatesGroupsAdmin(admin.ModelAdmin):
    list_filter = ['name',]
    search_fields = ['name']
    inlines = [RatesAdmin,]
    list_display = ['name', 'rate_type', 'rates_count']

    def save_model(self, request, obj, form, change):
        obj.user = request.user        
        #obj.customer = get_customer_by_user(request.user.id)
        obj.save()

    def save_formset(self, request, form, formset, change): # Procedimento para salvar as tags em string no campo tags_string
        formset.save()

        for f in formset.forms:
            list = ''
            obj = f.instance
            
            if f.has_changed():

                for tag in obj.tag.all():
                    list += str(tag.tag) + ','

                if (len(list) > 1): # Remove ultima virgula
                    list = list[:-1]

                obj.tags_string = list
                obj.save()
            

class InboundRoutesInline(admin.StackedInline):
    form = InboundRulesForm
    model = InboundRule
    fields = ('description', 'destination', 'weekdays', 'start', 'stop', 'specific_date',)
    verbose_name = 'Regra'
    verbose_name_plural = 'Regras'
    extra = 1


class InboundRoutesAdmin(admin.ModelAdmin):
    fields = ('description','provider', 'did')
    verbose_name = 'DID'
    verbose_name_plural = 'DID'

    inlines = [InboundRoutesInline,]    

    def save_model(self, request, obj, form, change):
        obj.user = request.user        
        #obj.customer = get_customer_by_user(request.user.id)
        obj.save()
                    
class CdrAdmin(admin.ModelAdmin):
    list_display = ['format_date', 'customer', 'device', 'destination_number', 'provider', 'lcr_name', 'billsec_datetime_format', 'user_cost', 'provider_cost', 'hangup_cause_and_q850', 'hangup_disposition', 'profit', 'details']
    list_filter = ('start_time', 'customer', 'provider', 'gateway',)
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def details(self,obj):
        return u'''
                <a href="/report/details/?uuid=%s" class="btn btn-small">
                    <i class="btn-icon-only icon-search"></i>Detalhes
                </a>
            ''' % (obj.uuid)

    details.allow_tags = True
    details.short_description = 'Detalhes'


    def billsec_datetime_format(self,obj):
        if obj.billsec:
            billsec = str(timedelta(seconds=int(obj.billsec)))
        else:
            billsec = 0

        return u'%s' % str(billsec)
        
    billsec_datetime_format.short_description = u'Duração'
    billsec_datetime_format.admin_order_field = 'billsec'

    def hangup_cause_and_q850(self,obj):
        return u'%s <%s>' % (obj.hangup_cause, obj.hangup_cause_q850)
        
    hangup_cause_and_q850.short_description = u'Hangup Cause'
    hangup_cause_and_q850.admin_order_field = 'hangup_cause'


    def profit(self,obj):
        return u'%s' % str(obj.user_cost - obj.provider_cost)
    
    profit.short_description = 'Lucro'    

    def format_date(self, obj):
        return obj.start_time.strftime('%d/%m/%Y %H:%M:%S')
    format_date.short_description = 'Date'


    def __init__(self, *args, **kwargs):
        super(CdrAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login', 'devices']

  
    verbose_name = ''
    verbose_name_plural = ''
    template = "admin/edit_inline/stacked_custom_user.html"
 
class CustomersAdmin(admin.ModelAdmin):
     #inlines = (UserInfo, CustomUsersInline,) - Manter para implementacao de revendas
 #   inlines = (UserInline, )
    list_display = ['name', 'customer_balance', 'postpaid_limit', 'max_calls', 'calls_per_second', 'lcr', 'rate_groups', 'devices']
    exclude = ('devices_limit',)
    readonly_fields = ['customer_balance',]
    formset_required = True
    form = CustomerForm
    def devices(self,obj): # Implementar filtros de devices por usuário
        return u'''
                <a href="/core/device/add/?customer=%s" class="btn btn-small">
                    <i class="btn-icon-only icon-plus"></i>Adicionar
                </a>

                <a href="/core/device/?customer=%s" class="btn btn-small">
                    <i class="btn-icon-only icon-search"></i>Listar
                </a>

            ''' % (obj.id, obj.id)

    devices.allow_tags = True
    devices.short_description = 'Devices'

    def save_model(self, request, obj, form, change):
        obj.save()
        parse_devices(None)

class CodecsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Blacklist, BlacklistAdmin)
admin.site.register(Device, DevicesAdmin)
admin.site.register(Provider, ProvidersAdmin)
admin.site.register(Lcr, LcrAdmin)
admin.site.register(DialruleGroup,DialrulesGroupsAdmin)
admin.site.register(RateTag, RateTagsAdmin)
admin.site.register(RateGroup,RatesGroupsAdmin)
admin.site.register(Cdr, CdrAdmin)
admin.site.register(Gateway, GatewaysAdmin)
admin.site.register(Codec, CodecsAdmin)
admin.site.register(InboundRoute,InboundRoutesAdmin)
admin.site.register(Customer, CustomersAdmin)
