from rest_framework import serializers
from machines.models import Machine #, LANGUAGE_CHOICES, STYLE_CHOICES

# an automatically determined set of fields
# simple default implementations for the create() and update() methods

class MachineSerializer(serializers.HyperlinkedModelSerializer):

	owner = serializers.ReadOnlyField(source='owner.username')
	# highlight = serializers.HyperlinkedIdentityField(view_name='machine-highlight', format='html')

	class Meta:
		model = Machine
		fields = ('id', 'alias', 'sn', 'os_name', 'os_version', 'comp_name', 'comp_version', 'state', 'owner')

		#fields = ('id', 'alias', 'sn', 'os_name', 'os_version', 'comp_name', 'comp_version', 'reports', 'lastest', 'state', 'owner')
		owner = serializers.ReadOnlyField(source='owner.username')

	'''
	def get_alias(self, obj):
		target_alias = Alias.objects.filter(id=obj.alias_id).first()

		serializer = AliasSerializer(target_alias)
		return serializer.data['name']

	

	def get_reports(self, obj):
		reports_num = TestRecord.objects.filter(test_machine_id=obj.id).count()
		return reports_num
	'''

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


class MachineHistoryRecordSerializer(serializers.ModelSerializer):

	machine_info = serializers.SerializerMethodField()
	reports = serializers.SerializerMethodField()
	branches = serializers.SerializerMethodField()

	class Meta:
		model = Machine
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
		target_machine = Machine.objects.filter(id=obj.id).first()
		serializer = MachineSerializer(target_machine)

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

