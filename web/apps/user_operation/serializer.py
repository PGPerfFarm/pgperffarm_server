from django.db.models import Count
from rest_framework import serializers

from test_records.serializer import TestRecordListSerializer
from users.serializer import AliasSerializer
from test_records.models import TestRecord
from users.models import UserMachine, Alias
import hashlib


class UserMachineManageSerializer(serializers.ModelSerializer):
    '''
    use UserMachineSerializer
    '''

    alias = serializers.SerializerMethodField()
    reports = serializers.SerializerMethodField()
    lastest = serializers.SerializerMethodField()

    class Meta:
        model = UserMachine
        fields = ('alias', 'os_name', 'os_version', 'comp_name', 'comp_version', 'reports', 'state', 'lastest')

    def get_alias(self, obj):
        target_alias = Alias.objects.filter(id=obj.alias_id).first()

        serializer = AliasSerializer(target_alias)
        return serializer.data['name']

    def get_reports(self, obj):
        reports_num = TestRecord.objects.filter(test_machine_id=obj.id).count()
        return reports_num

    def get_lastest(self, obj):
        record_branch_list = TestRecord.objects.filter(test_machine_id=obj.id).values_list(
            'branch').annotate(Count('id'))
        # < QuerySet[(1, 4), (2, 5)] >
        ret = []
        for branch_item in record_branch_list:
            branch_name = branch_item[0]

            target_record = TestRecord.objects.filter(test_machine_id=obj.id, branch=branch_item[0]).first()
            serializer = TestRecordListSerializer(target_record)

            dict = {'branch':branch_name,'record':serializer.data}

            ret.append(dict)

        return ret
