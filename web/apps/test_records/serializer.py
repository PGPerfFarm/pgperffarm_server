from rest_framework import serializers
from test_records.models import TestRecord, TestResult, PGInfo, LinuxInfo ,MetaInfo
from users.serializer import UserMachineSerializer
from users.models import UserMachine
from django.db.models import Q
class PGInfoSerializer(serializers.ModelSerializer):

    '''
    use ModelSerializer
    '''
    class Meta:
        model = PGInfo
        fields = "__all__"

class LinuxInfoSerializer(serializers.ModelSerializer):
    '''
    use ModelSerializer
    '''

    class Meta:
        model = LinuxInfo
        fields = "__all__"

class MetaInfoSerializer(serializers.ModelSerializer):

    '''
    use ModelSerializer
    '''
    class Meta:
        model = MetaInfo
        fields = "__all__"

class TestResultSerializer(serializers.ModelSerializer):

    '''
    use TestResultSerializer
    '''
    class Meta:
        model = TestResult
        fields = "__all__"

class TestRecordSerializer(serializers.ModelSerializer):

    '''
    use ModelSerializer
    '''
    pg_info =PGInfoSerializer()
    linux_info = LinuxInfoSerializer()
    meta_info = MetaInfoSerializer()
    ro_info = serializers.SerializerMethodField()
    rw_info = serializers.SerializerMethodField()
    machine_info = serializers.SerializerMethodField()
    client_max_num = serializers.SerializerMethodField()
    class Meta:
        model = TestRecord
        fields = ('add_time', 'machine_info', 'pg_info', 'linux_info', 'meta_info', 'ro_info', 'rw_info', 'client_max_num')

    def get_ro_info(self, obj):
        all_data = TestResult.objects.filter(Q(test_record_id=obj.id ) ,test_cate_id=1)

        ro_info_serializer = TestResultSerializer(all_data, many=True, context={'request': self.context['request']})
        return ro_info_serializer.data

    def get_rw_info(self, obj):
        all_data = TestResult.objects.filter(Q(test_record_id=obj.id) ,test_cate_id=2)

        rw_info_serializer = TestResultSerializer(all_data, many=True, context={'request': self.context['request']})
        return rw_info_serializer.data

    def get_machine_info(self, obj):
        machine_data = UserMachine.objects.filter(Q(id=obj.test_machine_id.id))

        machine_info_serializer = UserMachineSerializer(machine_data,many=True, context={'request': self.context['request']})
        return machine_info_serializer.data

    def get_client_max_num(self, obj):
        ro_client_num = TestResult.objects.filter(Q(test_record_id=obj.id ) ,test_cate_id=1).order_by('clients').distinct('clients').count()
        rw_client_num = TestResult.objects.filter(Q(test_record_id=obj.id ) ,test_cate_id=2).order_by('clients').distinct('clients').count()
        return max(ro_client_num,rw_client_num)

class TestRecordDetailSerializer(serializers.ModelSerializer):

    '''
    use ModelSerializer
    '''
    pg_info =PGInfoSerializer()
    linux_info = LinuxInfoSerializer()
    meta_info = MetaInfoSerializer()
    ro_info = serializers.SerializerMethodField()
    rw_info = serializers.SerializerMethodField()
    class Meta:
        model = TestRecord
        fields = "__all__"

    def get_ro_info(self, obj):
        all_data = TestResult.objects.filter(Q(test_record_id=obj.id ) ,test_cate_id=1)

        ro_info_serializer = TestResultSerializer(all_data, many=True, context={'request': self.context['request']})
        return ro_info_serializer.data

    def get_rw_info(self, obj):
        all_data = TestResult.objects.filter(Q(test_record_id=obj.id) ,test_cate_id=2)

        rw_info_serializer = TestResultSerializer(all_data, many=True, context={'request': self.context['request']})
        return rw_info_serializer.data
