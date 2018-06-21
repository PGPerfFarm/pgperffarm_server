from rest_framework import serializers
from users.models import UserMachine
from django.db.models import Q


class UserMachineSerializer(serializers.ModelSerializer):
    '''
    use UserMachineSerializer
    '''

    class Meta:
        model = UserMachine
        # fields = "__all__"
        fields = ('alias', 'os_name', 'os_version', 'comp_name', 'comp_version')
