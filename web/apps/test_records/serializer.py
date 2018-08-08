from rest_framework import serializers

from pgperffarm.settings import DB_ENUM
from test_records.models import TestRecord, TestResult, PGInfo, LinuxInfo, MetaInfo, TestDataSet, TestCategory, \
    TestBranch
from users.serializer import UserMachineSerializer
from users.models import UserMachine
from django.db.models import Count


class TestBranchSerializer(serializers.ModelSerializer):
    '''
    use TestBranchSerializer
    '''

    class Meta:
        model = TestBranch
        fields = ('branch_name', 'id')


class TestCategorySerializer(serializers.ModelSerializer):
    '''
    use TestCategorySerializer
    '''

    class Meta:
        model = TestCategory
        fields = ('cate_name', 'cate_sn')


class CreatePGInfoSerializer(serializers.ModelSerializer):
    '''
    use CreatePGInfoSerializer
    '''

    class Meta:
        model = PGInfo
        fields = "__all__"


class PGInfoSerializer(serializers.ModelSerializer):
    '''
    use PGInfoSerializer
            "settings": {
            "checkpoint_timeout": "15min",
            "log_temp_files": "32",
            "work_mem": "64MB",
            "log_line_prefix": "%n %t ",
            "shared_buffers": "1GB",
            "log_autovacuum_min_duration": "0",
            "checkpoint_completion_target": "0.9",
            "maintenance_work_mem": "128MB",
            "log_checkpoints": "on",
            "max_wal_size": "4GB",
            "min_wal_size": "2GB"
        }
    '''
    checkpoint_timeout = serializers.SerializerMethodField()
    work_mem = serializers.SerializerMethodField()
    shared_buffers = serializers.SerializerMethodField()
    maintenance_work_mem = serializers.SerializerMethodField()
    max_wal_size = serializers.SerializerMethodField()
    min_wal_size = serializers.SerializerMethodField()
    log_checkpoints = serializers.SerializerMethodField()

    class Meta:
        model = PGInfo
        fields = ('checkpoint_timeout', 'log_temp_files', 'work_mem', 'log_line_prefix', 'shared_buffers',
                  'log_autovacuum_min_duration', 'checkpoint_completion_target', 'maintenance_work_mem',
                  'log_checkpoints', 'max_wal_size', 'min_wal_size')

    def get_log_checkpoints(self, obj):
        new_dict = {v: k for k, v in DB_ENUM["general_switch"].items()}
        return new_dict[obj.log_checkpoints]

    def get_checkpoint_timeout(self, obj):
        return obj.checkpoint_timeout.__str__() + 'min'

    def get_work_mem(self, obj):
        return obj.work_mem.__str__() + 'MB'

    def get_shared_buffers(self, obj):
        return obj.shared_buffers.__str__() + 'GB'

    def get_maintenance_work_mem(self, obj):
        return obj.maintenance_work_mem.__str__() + 'MB'

    def get_max_wal_size(self, obj):
        return obj.max_wal_size.__str__() + 'GB'

    def get_min_wal_size(self, obj):
        return obj.min_wal_size.__str__() + 'GB'


class HardwareInfoDetailSerializer(serializers.ModelSerializer):
    '''
    use HardwareInfoDetailSerializer
    '''

    class Meta:
        model = LinuxInfo
        fields = ('cpuinfo', 'meminfo')


class LinuxInfoDetailSerializer(serializers.ModelSerializer):
    '''
    use LinuxInfoDetailSerializer
    '''

    class Meta:
        model = LinuxInfo
        fields = ('mounts', 'sysctl')


class LinuxInfoSerializer(serializers.ModelSerializer):
    '''
    use LinuxInfoSerializer
    '''

    class Meta:
        model = LinuxInfo
        fields = ('mounts', 'cpuinfo', 'sysctl', 'meminfo')


class MetaInfoDetailSerializer(serializers.ModelSerializer):
    '''
    use MetaInfoSerializer
    '''

    class Meta:
        model = MetaInfo
        fields = ('uname',)


class MetaInfoSerializer(serializers.ModelSerializer):
    '''
    use MetaInfoSerializer
    '''

    class Meta:
        model = MetaInfo
        fields = ('date', 'uname', 'benchmark', 'name')


class CreateTestResultSerializer(serializers.ModelSerializer):
    '''
    use CreateTestResultSerializer
    '''

    class Meta:
        model = TestResult
        fields = "__all__"


class TestResultSerializer(serializers.ModelSerializer):
    '''
    use TestResultSerializer
    '''
    mode = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = "__all__"

    def get_mode(self, obj):
        new_dict = {v: k for k, v in DB_ENUM["mode"].items()}
        return new_dict[obj.mode]


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


class TestStatusRecordListSerializer(serializers.ModelSerializer):
    '''
    use ModelSerializer
    '''
    pg_info = PGInfoSerializer()
    linux_info = LinuxInfoSerializer()
    meta_info = MetaInfoSerializer()
    branch = serializers.SerializerMethodField()
    trend = serializers.SerializerMethodField()
    machine_info = serializers.SerializerMethodField()

    # client_max_num = serializers.SerializerMethodField()
    class Meta:
        model = TestRecord
        fields = ('uuid', 'add_time', 'machine_info', 'pg_info', 'branch', 'trend', 'linux_info', 'meta_info')

    def get_branch(self, obj):
        branch = TestBranch.objects.filter(id=obj.branch.id).first()

        serializer = TestBranchSerializer(branch)
        return serializer.data["branch_name"]

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

        if (data_list_count == trend['none']):
            trend['is_first'] = True

        print str(data_list_count)
        return trend

    def get_machine_info(self, obj):
        machine_data = UserMachine.objects.filter(id=obj.test_machine_id)

        machine_info_serializer = UserMachineSerializer(machine_data, many=True)
        return machine_info_serializer.data

    # def get_client_max_num(self, obj):
    #     ro_client_num = TestResult.objects.filter(Q(test_record_id=obj.id ) ,test_cate_id=1).order_by('clients').distinct('clients').count()
    #     rw_client_num = TestResult.objects.filter(Q(test_record_id=obj.id ) ,test_cate_id=2).order_by('clients').distinct('clients').count()
    #     return max(ro_client_num,rw_client_num)


class TestRecordListSerializer(serializers.ModelSerializer):
    '''
    use ModelSerializer
    '''
    # pg_info = PGInfoSerializer()
    linux_info = LinuxInfoSerializer()
    meta_info = MetaInfoSerializer()
    branch = serializers.SerializerMethodField()
    trend = serializers.SerializerMethodField()
    machine_info = serializers.SerializerMethodField()

    # client_max_num = serializers.SerializerMethodField()
    class Meta:
        model = TestRecord
        fields = ('uuid', 'add_time', 'machine_info', 'branch', 'trend', 'linux_info', 'meta_info', 'commit')

    def get_branch(self, obj):
        branch = TestBranch.objects.filter(id=obj.branch.id).first()

        serializer = TestBranchSerializer(branch)
        return serializer.data["branch_name"]

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

        if (data_list_count == trend['none']):
            trend['is_first'] = True

        print str(data_list_count)
        return trend

    def get_machine_info(self, obj):
        machine_data = UserMachine.objects.filter(id=obj.test_machine_id).get()

        machine_info_serializer = UserMachineSerializer(machine_data)
        return machine_info_serializer.data

    # def get_client_max_num(self, obj):
    #     ro_client_num = TestResult.objects.filter(Q(test_record_id=obj.id ) ,test_cate_id=1).order_by('clients').distinct('clients').count()
    #     rw_client_num = TestResult.objects.filter(Q(test_record_id=obj.id ) ,test_cate_id=2).order_by('clients').distinct('clients').count()
    #     return max(ro_client_num,rw_client_num)


class TestDataSetDetailSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()

    class Meta:
        model = TestDataSet
        fields = "__all__"

    def get_results(self, obj):
        all_data = TestResult.objects.filter(test_dataset=obj.id)

        serializer = TestResultSerializer(all_data, many=True)
        return serializer.data


class TestRecordDetailSerializer(serializers.ModelSerializer):
    '''
    use ModelSerializer
    '''
    branch = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    pg_info = PGInfoSerializer()
    linux_info = LinuxInfoDetailSerializer()
    test_machine = UserMachineSerializer()
    hardware_info = serializers.SerializerMethodField()
    meta_info = MetaInfoDetailSerializer()
    dataset_info = serializers.SerializerMethodField()

    prev = serializers.SerializerMethodField()
    class Meta:
        model = TestRecord
        fields = (
            'branch', 'date', 'uuid', 'pg_info', 'linux_info', 'hardware_info', 'meta_info', 'dataset_info',
            'test_desc', 'meta_time', 'test_machine', 'commit', 'prev')

    def get_prev(self, obj):
        target = TestDataSet.objects.filter(test_record_id=obj.id).first()
        serializer = TestDataSetDetailSerializer(target)
        prev = serializer.data["prev"]
        target = TestDataSet.objects.filter(id=prev).first()
        serializer = TestDataSetDetailSerializer(target)
        record_id =  serializer.data["test_record"]

        target_record= TestRecord.objects.filter(id=record_id).first()
        serializer = TestRecordDetailSerializer(target_record)
        return serializer.data["uuid"]

    def get_branch(self, obj):
        branch = TestBranch.objects.filter(id=obj.branch_id).first()

        serializer = TestBranchSerializer(branch)
        return serializer.data["branch_name"]

    def get_date(self, obj):
        target_meta_info = MetaInfo.objects.filter(id=obj.meta_info.id).first()

        return target_meta_info.date

    def get_hardware_info(self, obj):
        target_data = LinuxInfo.objects.filter(id=obj.linux_info.id).first()

        hardware_info_serializer = HardwareInfoDetailSerializer(target_data)
        return hardware_info_serializer.data

    def get_dataset_info(self, obj):
        dataset_list = TestDataSet.objects.filter(test_record_id=obj.id).values_list('test_cate_id').annotate(
            Count('id'))
        # print(dataset_list)

        dataset = {}
        # < QuerySet[(1, 3), (2, 3)] >

        for cate_item in dataset_list:

            cate_info = TestCategory.objects.filter(id=cate_item[0]).first()
            cate_info_serializer = TestCategorySerializer(cate_info)
            cate_sn = cate_info_serializer.data["cate_sn"]
            dataset[cate_sn] = {}

            dataset_scale_list = TestDataSet.objects.filter(test_record_id=obj.id, test_cate=cate_item[0]).values_list(
                'scale').annotate(Count('id'))
            # print(dataset_scale_list) # <QuerySet [(10, 2), (20, 1)]>
            for scale_item in dataset_scale_list:
                dataset[cate_sn][scale_item[0]] = {}

                dataset_client_list = TestDataSet.objects.filter(test_record_id=obj.id,
                                                                 test_cate=cate_item[0],
                                                                 scale=scale_item[0]).values_list(
                    'clients').annotate(Count('id'))
                # print(dataset_client_list) # <QuerySet [(1, 1), (2, 1), (4, 1)]>
                for client_item in dataset_client_list:
                    dataset[cate_sn][scale_item[0]][client_item[0]] = []
                    target_dataset = TestDataSet.objects.filter(test_record_id=obj.id, test_cate=cate_item[0],
                                                                scale=scale_item[0], clients=client_item[0])

                    dataset_serializer = TestDataSetDetailSerializer(target_dataset, many=True)
                    dataset[cate_sn][scale_item[0]][client_item[0]] = dataset_serializer.data

        return dataset


class MachineHistoryRecordSerializer(serializers.ModelSerializer):
    '''
    use MachineHistoryRecordSerializer
    '''
    machine_info = serializers.SerializerMethodField()
    reports = serializers.SerializerMethodField()
    branches = serializers.SerializerMethodField()

    class Meta:
        model = UserMachine
        fields = ('machine_info', 'reports', 'branches')

    def get_reports(self, obj):
        target_records = TestRecord.objects.filter(test_machine_id=obj.id).values_list(
            'branch').annotate(Count('id'))
        # print(target_records) # <QuerySet [(2, 2), (1, 3)]>
        ret = []
        for branch_item in target_records:
            item = {}
            item['branch'] = branch_item[0]

            records = TestRecord.objects.filter(test_machine_id=obj.id, branch_id=branch_item[0])

            serializer = TestRecordListSerializer(records, many=True)
            item['records'] = serializer.data
            ret.append(item)
        return ret

    def get_machine_info(self, obj):
        target_machine = UserMachine.objects.filter(id=obj.id).first()
        serializer = UserMachineSerializer(target_machine)

        return serializer.data

    def get_branches(self, obj):
        target_records = TestRecord.objects.filter(test_machine_id=obj.id).values_list(
            'branch').annotate(Count('id'))

        ret = []
        for branch_item in target_records:
            item = {}
            item['value'] = branch_item[0]

            branch = TestBranch.objects.filter(id=branch_item[0]).first()
            serializer = TestBranchSerializer(branch)
            item['branch'] = serializer.data["branch_name"]
            ret.append(item)

        return ret
