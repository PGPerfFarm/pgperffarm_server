from rest_framework import serializers

from pgperffarm.settings import AVATAR_URL
from test_records.models import TestRecord
from users.models import UserMachine, Alias, UserProfile
import hashlib

class AliasSerializer(serializers.ModelSerializer):
    '''
    use TestResultSerializer
    '''

    class Meta:
        model = Alias
        fields = ('name', )

class CreateUserProfileSerializer(serializers.ModelSerializer):
    '''
    use CreateUserProfileSerializer
    '''
    class Meta:
        model = UserProfile
        fields = "__all__"

class UserMachineSerializer(serializers.ModelSerializer):
    '''
    use UserMachineSerializer
    '''

    alias = serializers.SerializerMethodField()
    reports = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = UserMachine
        fields = ('alias', 'os_name', 'os_version', 'comp_name', 'comp_version', 'reports', 'owner' , 'avatar', 'machine_sn')

    def get_alias(self, obj):
        target_alias = Alias.objects.filter(id=obj.alias_id).first()

        serializer = AliasSerializer(target_alias)
        return serializer.data['name']

    def get_reports(self, obj):
        reports_num = TestRecord.objects.filter(test_machine_id=obj.id).count()
        return reports_num

    def get_owner(self, obj):
        target_owner = UserProfile.objects.filter(id=obj.machine_owner_id).first()
        serializer = JWTUserProfileSerializer(target_owner)
        return serializer.data

    def get_avatar(self, obj):
        target_owner = UserProfile.objects.filter(id=obj.machine_owner_id).values('email').first()


        avatar = AVATAR_URL + hashlib.md5(target_owner['email']).hexdigest()
        return  avatar

class JWTUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email')