from machines.models import Machine, Alias
from machines.serializers import MachineSerializer, AliasSerializer
from users.serializers import UserSerializer
from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status
from machines.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.models import User


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

		username = serializers.ReadOnlyField(source='owner.username')
		#username = request.data['machine_owner.username']
		user = User.objects.filter(username=username).filter().first()
		user_serializer = UserSerializer(user)

		data['owner'] = user_serializer.data['username']

		serializer = MachineSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		machine = self.perform_create(serializer)

		headers = self.get_success_headers(serializer.data)

		return Response('success', status=status.HTTP_201_CREATED, headers=headers)

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
