from postgres.models import PostgresSettingsSet, PostgresSettings
from postgres.serializers import PostgresSettingsSetSerializer, PostgresSettingsSerializer

from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status


class PostgresSettingsSetViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PostgresSettingsSet.objects.all()
	serializer_class = PostgresSettingsSetSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class PostgresSettingsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PostgresSettings.objects.all()
	serializer_class = PostgresSettingsSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )