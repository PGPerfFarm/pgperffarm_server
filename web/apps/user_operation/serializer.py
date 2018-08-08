from django.db.models import Count
from rest_framework import serializers

from pgperffarm.settings import DB_ENUM,AVATAR_URL
from test_records.serializer import TestRecordListSerializer
from users.serializer import AliasSerializer, UserMachineSerializer
from test_records.models import TestRecord
from users.models import UserMachine, Alias, UserProfile
import hashlib


class UserPortalInfoSerializer(serializers.ModelSerializer):
    involved = serializers.SerializerMethodField()
    reports = serializers.SerializerMethodField()
    machines = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('email', 'involved', 'reports', 'date_joined', 'machines', 'avatar')

    def date_joined(self, obj):
        return obj.date_joined.strftime('%Y')

    def get_avatar(self, obj):
        email = obj.email
        avatar = AVATAR_URL + hashlib.md5(email).hexdigest()
        return avatar

    def get_machines(self, obj):
        '''
        machines num
        '''

        return UserMachine.objects.filter(machine_owner_id=obj.id).count()

    def get_reports(self, obj):
        '''
        reports num
        '''
        machine_dict = []
        target_machines = UserMachine.objects.filter(machine_owner_id=obj.id)
        serializer = UserMachineSerializer(target_machines, many=True)
        # print(serializer.data)
        for item in serializer.data:
            machine_dict.append(item['machine_sn'])

        reports = TestRecord.objects.filter(test_machine__machine_sn__in=machine_dict).count()

        return reports

    def get_involved(self, obj):
        '''
        reports, machines, branches
        '''
        machine_dict = []
        target_machines = UserMachine.objects.filter(machine_owner_id=obj.id)
        serializer = UserMachineSerializer(target_machines, many=True)
        # print(serializer.data)
        for item in serializer.data:
            machine_dict.append(item['machine_sn'])

        reports = TestRecord.objects.filter(test_machine__machine_sn__in=machine_dict).values_list('branch__branch_name').annotate(Count('id'))
        return reports.count()


class UserMachineManageSerializer(serializers.ModelSerializer):
    '''
    use UserMachineSerializer
    '''

    alias = serializers.SerializerMethodField()
    reports = serializers.SerializerMethodField()
    lastest = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = UserMachine
        fields = (
        'alias', 'machine_sn', 'os_name', 'os_version', 'comp_name', 'comp_version', 'reports', 'state', 'lastest',
        'state', 'add_time')

    def get_state(self, obj):
        state_code = obj.state
        new_dict = {v: k for k, v in DB_ENUM["machine_state"].items()}
        return new_dict[state_code]

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
            # branch_name = branch_item[0]

            target_record = TestRecord.objects.filter(test_machine_id=obj.id, branch=branch_item[0]).first()
            serializer = TestRecordListSerializer(target_record)

            ret.append(serializer.data)

        return ret
