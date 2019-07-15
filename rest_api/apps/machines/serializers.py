from rest_framework import serializers
from machines.models import Machine #, LANGUAGE_CHOICES, STYLE_CHOICES

# an automatically determined set of fields
# simple default implementations for the create() and update() methods

class MachineSerializer(serializers.HyperlinkedModelSerializer):

	owner = serializers.ReadOnlyField(source='owner.username')
	# highlight = serializers.HyperlinkedIdentityField(view_name='machine-highlight', format='html')

	class Meta:
		model = Machine
		fields = ('id', 'alias', 'sn', 'os_name', 'os_version', 'comp_name', 'comp_version', 'reports', 'lastest', 'state', 'owner')
		owner = serializers.ReadOnlyField(source='owner.username')



