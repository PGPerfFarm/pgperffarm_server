import django_filters
import shortuuid
import json
from rest_framework import serializers

from runs.models import RunInfo


class RuntimeSerializer(serializers.ModelSerializer):

	run_received_time = serializers.DateTimeField()
	run_start_time = serializers.DateTimeField()
	run_end_time = serializers.SerializerMethodField()

	git_clone_runtime = serializers.FloatField()
	
	configure_runtime = serializers.FloatField()
	build_runtime = serializers.FloatField()
	install_runtime = serializers.FloatField()
	cleanup_runtime = serializers.FloatField()

    class Meta:
        model = RunInfo
        fields = ['run_received_time', 'run_start_time', 'run_end_time', 'git_clone_runtime', 'configure_runtime', 'build_runtime', 'install_runtime', 'cleanup_runtime']

    
class RunInfoSerializer(serializers.ModelSerializer):

	class Meta:
        model = RunInfo