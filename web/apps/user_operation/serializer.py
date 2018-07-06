from rest_framework import serializers

from users.serializer import AliasSerializer
from test_records.models import TestRecord
from users.models import UserMachine, Alias, UserProfile
import hashlib

class UserMachineManageSerializer(serializers.ModelSerializer):
    '''
    use UserMachineSerializer
    '''

    alias = serializers.SerializerMethodField()
    reports = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = UserMachine
        fields = ('alias', 'os_name', 'os_version', 'comp_name', 'comp_version', 'reports', 'owner' , 'avatar', 'state')

    def get_alias(self, obj):
        target_alias = Alias.objects.filter(id=obj.alias_id).first()

        serializer = AliasSerializer(target_alias)
        return serializer.data['name']

    def get_reports(self, obj):
        reports_num = TestRecord.objects.filter(test_machine_id=obj.id).count()
        return reports_num

    def get_owner(self, obj):
        target_owner = UserProfile.objects.filter(id=obj.machine_owner_id).values('email').first()

        return target_owner['email']

    def get_avatar(self, obj):
        target_owner = UserProfile.objects.filter(id=obj.machine_owner_id).values('email').first()

        avatar = 'http://s.gravatar.com/avatar/' + hashlib.md5(target_owner['email']).hexdigest()
        print avatar
        return  avatar
