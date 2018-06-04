from rest_framework import serializers
from test_records.models import TestRecord, TestResult, PGInfo, LinuxInfo ,MetaInfo
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

    # test_machine_id = serializers.ForeignKey(UserMachine, verbose_name="test owner",
    #                                     help_text="person who add this test item")
    # pg_info = serializers.ForeignKey(PGInfo, verbose_name="pg info", help_text="pg info")
    # meta_info = serializers.ForeignKey(MetaInfo, verbose_name="meta info", help_text="meta info")

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return TestRecord.objects.create(**validated_data)
