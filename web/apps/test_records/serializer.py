from rest_framework import serializers
from .models import TestRecord
class TestRecordSerializer(serializers.ModelSerializer):

    '''
    use ModelSerializer
    '''
    class Meta:
        model = TestRecord
        fields = "__all__"

    # test_machine_id = serializers.ForeignKey(UserMachine, verbose_name="test owner",
    #                                     help_text="person who add this test item")
    # pg_info = serializers.ForeignKey(PGInfo, verbose_name="pg info", help_text="pg info")
    # meta_info = serializers.ForeignKey(MetaInfo, verbose_name="meta info", help_text="meta info")

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return TestRecord.objects.create(**validated_data)