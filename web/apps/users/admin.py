# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from serializer import UserMachineSerializer
from .models import UserMachine

class UserMachineAdmin(admin.ModelAdmin):
    list_display = ('alias', 'machine_sn', 'state')
    list_filter = ('state',)
    actions = ['approve_machine']

    def approve_machine(self, request, queryset):

        total = 0
        error = 0
        success =0
        for machine in queryset:

            ret = machine.approve_machine()
            '''
                ret = {"is_success": True, "alias": 'alias', "secrct": 'machine_secret', }
            '''
            if ret.is_success:
                success += 1
            else:
                error += 1

            total +=1

        # rows_updated = queryset.update(state=1)
        # message_bit = "%s machine(s)" % rows_updated
        self.message_user(request, "Total: %s ,Success: %s ,Error: %s. Please make sure there are enough unused aliases" % (total,success,error))

    approve_machine.short_description = u'Approve Machine(Modify the state to active, generate machine_sn, machine_secret, and assign an alias)'


admin.site.register(UserMachine, UserMachineAdmin)
