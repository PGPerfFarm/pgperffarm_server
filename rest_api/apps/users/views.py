import django_filters

from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, viewsets, generics, views, mixins, authentication, response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import list_route
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from users.serializers import UserSerializer
from machines.models import Machine
from machines.serializers import MachineSerializer
from records.models import TestRecord
from records.serializers import TestRecordListSerializer
from users.filters import UserMachineListFilter, MachineRecordListFilter


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""

	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = UserSerializer
	queryset = User.objects.all().order_by('-date_joined')
	lookup_field = ('username')


class UserMachineRecordByBranchListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
	List machine records by branch
	"""
	queryset = TestRecord.objects.all().order_by('-add_time')
	serializer_class = TestRecordListSerializer
	filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class UserMachineListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
	"""
	List test records
	"""
	authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Machine.objects.all().order_by('added')
	serializer_class = MachineSerializer
	filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
	filter_class = UserMachineListFilter

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def create(self, request, *args, **kwargs):
		data = {}
		data['os_name'] = request.data['os_name']
		data['os_version'] = request.data['os_version']
		data['comp_name'] = request.data['comp_name']
		data['comp_version'] = request.data['comp_version']

		username = request.data['machine_owner']
		user = User.objects.filter(username=username).filter().first()
		user_serializer = UserSerializer(user)

		data['machine_owner'] = user_serializer.data['id']

		serializer = MachineSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		machine = self.perform_create(serializer)

		headers = self.get_success_headers(serializer.data)

		return Response('success', status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		return serializer.save()


class UserMachinePermission(permissions.BasePermission):
	"""
	Machine upload permission check
	"""
	def has_permission(self, request, view):
		secret = request.META.get("HTTP_AUTHORIZATION")
		# print(secret)
		# alias = request.data.alias
		ret = Machine.objects.filter(machine_secret=secret, state=1).exists()
		return ret