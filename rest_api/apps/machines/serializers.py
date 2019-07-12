from rest_framework import serializers
from machines.models import Machine #, LANGUAGE_CHOICES, STYLE_CHOICES

# an automatically determined set of fields
# simple default implementations for the create() and update() methods

class MachineSerializer(serializers.Serializer):

	class Meta:
		model = Machine
		fields = ('id', 'alias', 'sn', 'os_name', 'os_version', 'comp_name', 'comp_version', 'reports', 'lastest', 'state')
