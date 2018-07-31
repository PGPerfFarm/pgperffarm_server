# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from serializer import UserMachineSerializer
from .models import UserMachine,Alias

class UserMachineAdmin(admin.ModelAdmin):
    list_display = ('alias', 'machine_sn', 'state')
    list_filter = ('state',)
    actions = ['approve_machine']

    def approve_machine(self, request, queryset):
        for machine in queryset:
            alias = Alias.objects.filter(is_used=False).order_by('?')[:1]
            #todo
            serializer = UserMachineSerializer(machine)
            serializer.save()

        # rows_updated = queryset.update(state=1)
        # message_bit = "%s machine(s)" % rows_updated
        # self.message_user(request, "%s have been approved." % message_bit)

    approve_machine.short_description = u'Approve Machine(Modify the state to active, generate machine_sn, machine_secret, and assign an alias)'


admin.site.register(UserMachine, UserMachineAdmin)
