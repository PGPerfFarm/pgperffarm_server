from systems.models import HardwareInfo, Compiler
from systems.serializers import HardwareInfoSerializer, CompilerSerializer

from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status


class SystemViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  HardwareInfo.objects.all().order_by('linux_info_id')
	serializer_class = HardwareInfoSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class CompilerViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  Compiler.objects.all().order_by('compiler_id')
	serializer_class = CompilerSerializer