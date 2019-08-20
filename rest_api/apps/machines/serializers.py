from rest_framework import serializers
from django.db.models import Count
from machines.models import Machine, Alias
from django.contrib.auth.models import User

# an automatically determined set of fields
# simple default implementations for the create() and update() methods

class MachineSerializer(serializers.ModelSerializer):

	reports = serializers.SerializerMethodField()
	owner_email = serializers.ReadOnlyField()
	owner_username = serializers.ReadOnlyField()
	alias = serializers.SerializerMethodField()
	sn = serializers.ReadOnlyField()
	lastest = serializers.SerializerMethodField()

	class Meta:
		model = Machine
		fields = ('alias', 'os_name', 'os_version', 'comp_name', 'comp_version', 'reports', 'owner_username', 'owner_email', 'sn', 'lastest', 'add_time', 'state')


	def get_alias(self, obj):
		target_alias = Alias.objects.filter(name=obj.alias).first()

		serializer = AliasSerializer(target_alias)
		return serializer.data['name']


	def get_reports(self, obj):
		from records.models import TestRecord
		reports_num = TestRecord.objects.filter(test_machine_id=obj.id).count()
		return reports_num

	def get_lastest(self, obj):
		from records.models import TestRecord
		from records.serializers import TestRecordLastestSerializer
		record_branch_list = TestRecord.objects.filter(test_machine_id=obj.id).values_list(
			'branch').annotate(Count('id'))
		# < QuerySet[(1, 4), (2, 5)] >
		ret = []
		for branch_item in record_branch_list:
			# branch_name = branch_item[0]

			target_record = TestRecord.objects.filter(test_machine_id=obj.id, branch=branch_item[0]).first()
			serializer = TestRecordLastestSerializer(target_record)

			ret.append(serializer.data)

		return ret


class MachineRecordSerializer(serializers.ModelSerializer):

	reports = serializers.SerializerMethodField()
	owner_username = serializers.ReadOnlyField()
	owner_email = serializers.ReadOnlyField()
	alias = serializers.SerializerMethodField()
	sn = serializers.ReadOnlyField()
	state = serializers.ReadOnlyField()


	class Meta:
		model = Machine
		fields = ('alias', 'os_name', 'os_version', 'comp_name', 'comp_version', 'reports', 'owner_username', 'owner_email', 'sn', 'state')


	def get_alias(self, obj):
		target_alias = Alias.objects.filter(name=obj.alias).first()

		serializer = AliasSerializer(target_alias)
		return serializer.data['name']


	def get_reports(self, obj):
		from records.models import TestRecord
		reports_num = TestRecord.objects.filter(test_machine_id=obj.id).count()
		return reports_num


class UserMachineSerializer(serializers.ModelSerializer):

	reports = serializers.SerializerMethodField()
	owner_username = serializers.ReadOnlyField()
	owner_id = serializers.ReadOnlyField(source='owner.id')
	owner_email = serializers.ReadOnlyField()
	state = serializers.ReadOnlyField()
	alias = serializers.SerializerMethodField()
	sn = serializers.ReadOnlyField()
	machine_secret = serializers.ReadOnlyField()
	lastest = serializers.SerializerMethodField()

	class Meta:
		model = Machine
		fields = '__all__'

	def get_alias(self, obj):
		target_alias = Alias.objects.filter(name=obj.alias).first()

		serializer = AliasSerializer(target_alias)
		return serializer.data['name']


	def get_reports(self, obj):
		from records.models import TestRecord
		reports_num = TestRecord.objects.filter(test_machine_id=obj.id).count()
		return reports_num

	def get_lastest(self, obj):
		from records.models import TestRecord
		from records.serializers import TestRecordLastestSerializer
		record_branch_list = TestRecord.objects.filter(test_machine_id=obj.id).values_list(
			'branch').annotate(Count('id'))
		# < QuerySet[(1, 4), (2, 5)] >
		ret = []
		for branch_item in record_branch_list:
			# branch_name = branch_item[0]

			target_record = TestRecord.objects.filter(test_machine_id=obj.id, branch=branch_item[0]).first()
			serializer = TestRecordLastestSerializer(target_record)

			ret.append(serializer.data)

		return ret


class AliasSerializer(serializers.ModelSerializer):

	class Meta:
		model = Alias
		fields = ('name', 'is_used')


