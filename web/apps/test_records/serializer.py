from rest_framework import serializers

from pgperffarm.settings import DB_ENUM
from test_records.models import TestRecord, TestResult, PGInfo, LinuxInfo ,MetaInfo, TestDataSet
from users.serializer import UserMachineSerializer
from users.models import UserMachine
from django.db.models import Q, QuerySet, Count


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

class CreateTestRecordSerializer(serializers.ModelSerializer):

    '''
    create ModelSerializer
    '''
    # pg_info =PGInfoSerializer()
    # linux_info = LinuxInfoSerializer()
    # meta_info = MetaInfoSerializer()

    class Meta:
        model = TestRecord
        fields = "__all__"

class CreateTestDateSetSerializer(serializers.ModelSerializer):

    '''
    create TestDateSetSerializer
        'test_record': testRecordRet.id,
        'clients': client_num,
        'scale': scale,
        'std': dataset['std'],
        'metric': dataset['metric'],
        'median': dataset['median'],
        'test_cate': test_cate.id,
        # status,percentage calc by tarr
        'status': -1,
        'percentage': 0.0,
    '''

    class Meta:
        model = TestDataSet
        fields = "__all__"

class TestRecordListSerializer(serializers.ModelSerializer):

    '''
    use ModelSerializer
    '''
    pg_info =PGInfoSerializer()
    linux_info = LinuxInfoSerializer()
    meta_info = MetaInfoSerializer()

    trend = serializers.SerializerMethodField()
    machine_info = serializers.SerializerMethodField()
    # client_max_num = serializers.SerializerMethodField()
    class Meta:
        model = TestRecord
        fields = ('add_time', 'machine_info', 'pg_info', 'trend', 'linux_info', 'meta_info')

    def get_trend(self, obj):
        dataset_list = TestDataSet.objects.filter(test_record_id=obj.id).values_list('status').annotate(Count('id'))
        data_list_count = TestDataSet.objects.filter(test_record_id=obj.id).count()

        trend = {}
        trend['improved'] = 0
        trend['quo'] = 0
        trend['regressive'] = 0
        trend['none'] = 0
        trend['is_first'] = False
        for i in dataset_list:
            if i[0] == DB_ENUM['status']['improved']:
                trend['improved'] += i[1]
            elif i[0] == DB_ENUM['status']['quo']:
                trend['quo'] += i[1]
            elif i[0] == DB_ENUM['status']['regressive']:
                trend['regressive'] += i[1]
            elif i[0] == DB_ENUM['status']['none']:
                trend['none'] += i[1]

        if(data_list_count == trend['none']):
            trend['is_first'] = True

        print str(data_list_count)
        return trend


    def get_machine_info(self, obj):
        machine_data = UserMachine.objects.filter(Q(id=obj.test_machine_id))

        machine_info_serializer = UserMachineSerializer(machine_data,many=True, context={'request': self.context['request']})
        return machine_info_serializer.data

    # def get_client_max_num(self, obj):
    #     ro_client_num = TestResult.objects.filter(Q(test_record_id=obj.id ) ,test_cate_id=1).order_by('clients').distinct('clients').count()
    #     rw_client_num = TestResult.objects.filter(Q(test_record_id=obj.id ) ,test_cate_id=2).order_by('clients').distinct('clients').count()
    #     return max(ro_client_num,rw_client_num)

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
