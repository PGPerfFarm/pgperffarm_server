from machines.models import Machine, Alias
from machines.serializers import MachineSerializer, AliasSerializer
from users.serializers import UserSerializer
from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status
from machines.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
import shortuuid
import hashlib
from django.contrib.auth.hashers import make_password


class UserMachineViewSet(viewsets.ModelViewSet):

	authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication, )
	permission_classes = (permissions.IsAuthenticated, )
	queryset = Machine.objects.all().order_by('add_time')
	serializer_class = MachineSerializer
	'''
	pagination_class = MiddleResultsSetPagination
	filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
	filter_class = UserMachineListFilter
	'''

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def create(self, request, *args, **kwargs):
		data = {}
		data['os_name'] = request.data['os_name']
		data['os_version'] = request.data['os_version']
		data['comp_name'] = request.data['comp_name']
		data['comp_version'] = request.data['comp_version']

		owner = self.request.user

		user = User.objects.get(username=owner)
		user_serializer = UserSerializer(user, context={'request': request})

		data['owner_username'] = user_serializer.data['username']
		data['owner_email'] = user_serializer.data['email']

		alias = Alias.objects.filter(is_used=False).order_by('?').first()
		
		# if not alias:
			# return {"is_success": False, "alias": '', "secret": '', "email": ''}
		

		from django.db import transaction
		with transaction.atomic():
			#alias.is_used = True
			#alias.save()

			data['alias'] = alias.name
			data['state'] = 1

			data['sn'] = shortuuid.ShortUUID().random(length=16)

			machine_str = str(data)

		m = hashlib.md5()
		m.update(make_password(str(machine_str), 'pg_perf_farm').encode('utf-8'))
		data['machine_secret'] = m.hexdigest()

		serializer = MachineSerializer(data=data)
		serializer.is_valid(raise_exception=True)

		machine = self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)

		return Response('Machine added successfully!', status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		return serializer.save()


class MachineViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
	List all machines
	"""
	queryset =  Machine.objects.all().order_by('add_time')
	serializer_class = MachineSerializer


class AliasViewSet(viewsets.ModelViewSet):
	"""
	List all aliases
	"""
	queryset =  Alias.objects.all().order_by('add_time')
	serializer_class = AliasSerializer


class UserMachinePermission(permissions.BasePermission):
	"""
	Machine upload permission check
	"""

	def has_permission(self, request, view):
		secret = request.META.get("HTTP_AUTHORIZATION")
		# print(secret)
		# alias = request.data.alias
		ret = UserMachine.objects.filter(machine_secret=secret, state=1).exists()
		return ret
