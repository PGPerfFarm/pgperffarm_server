from postgres.models import PostgresSettingsSet
from postgres.serializers import PostgresSettingsSetSerializer

from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status


class PostgresSettingsSetViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PostgresSettingsSet.objects.all()
	serializer_class = PostgresSettingsSetSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )