from machines.models import Machine, Alias
from machines.serializers import MachineSerializer, AliasSerializer, UserMachineSerializer
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
	serializer_class = UserMachineSerializer
	lookup_field = 'sn'


	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def create(self, request, *args, **kwargs):

		alias = Alias.objects.filter(is_used=False).order_by('?').first()
		
		if not alias:
			return Response('Alias not available!', status=status.HTTP_406_NOT_ACCEPTABLE)
		
		from django.db import transaction
		with transaction.atomic():
			alias.is_used = True
			alias.save()

		sn = shortuuid.ShortUUID().random(length=16)

		machine_str = 'test'

		m = hashlib.md5()
		m.update(make_password(str(machine_str), 'pg_perf_farm').encode('utf-8'))
		machine_secret = m.hexdigest()

		serializer = MachineSerializer(data=self.request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(
			owner_username=self.request.user, 
			owner_email=self.request.user.email, 
			alias=alias.name, 
			sn=sn,
			machine_secret=machine_secret,
			state='A'
			)

		headers = self.get_success_headers(serializer.data)
		return Response('Machine added successfully!', status=status.HTTP_201_CREATED, headers=headers)


class MachineViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
	List all machines
	"""
	queryset =  Machine.objects.all().order_by('add_time')
	serializer_class = MachineSerializer
	lookup_field = 'sn'
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


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
