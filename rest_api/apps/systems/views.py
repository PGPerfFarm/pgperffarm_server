from systems.models import LinuxInfo
from systems.serializers import LinuxInfoSerializer

from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status


class SystemViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
	List all machines
	"""
	queryset =  LinuxInfo.objects.all().order_by('linux_info_id')
	serializer_class = LinuxInfoSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )