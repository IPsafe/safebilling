# -*- coding: utf-8 -*-

from ipsafe.ipbx.models import *
from ipsafe.ipbx.views import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ConferenceAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_filter = ('id', 'confno', 'name')
    search_fields = ['id', 'confno', 'name']
    
    fieldsets = (
        ('', {
            'fields': ['name',('confno', 'pin'),],
        }),
        (u'Avançado', {
            'classes': ('collapse closed',),
            'fields' : (('starttime','endtime'), 'opts', 'adminpin', 'adminopts', 'members','maxusers')
            },
         ),
        )

class PickupGroupsAdmin(admin.ModelAdmin):
    pass

class QueuesMembersAdmin(admin.TabularInline):
    model = QueueMembers
    sortable_field_name = 'penalty'
    fieldsets = (
        ('', {
            'fields': ['interface', 'penalty',],
        }),
    )
    
    
class QueuesAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    classes = ('collapse closed',)
    fieldsets = (
        ('', {
            'fields': ['name', 'description', 'musiconhold'],
        }),
        (u'Avançado', {
            'classes': ('collapse closed',),
            'fields' : ('announce', 'context', 'timeout', 'monitor_join', 'monitor_format', 'queue_youarenext', 'queue_thereare', 'queue_callswaiting', 'queue_holdtime', 'queue_minutes',
                        'queue_seconds', 'queue_lessthan', 'queue_reporthold', 'announce_frequency', 'announce_round_seconds', 'announce_holdtime', 'retry', 'wrapuptime', 'maxlen', 'servicelevel',
                        'strategy', 'joinempty', 'leavewhenempty', 'eventmemberstatus', 'eventwhencalled', 'reportholdtime', 'memberdelay', 'weight', 'timeoutrestart', 'setinterfacevar'),
        }),
                 
    )
  
    list_display = ('name', 'description',)
    list_filter = ('name', 'description',)
    search_fields = ['name', 'description',]
    inlines = [QueuesMembersAdmin,]
    
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('name',) + self.readonly_fields
        return self.readonly_fields
    


admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Queues, QueuesAdmin)
admin.site.register(PickupGroups,PickupGroupsAdmin)
