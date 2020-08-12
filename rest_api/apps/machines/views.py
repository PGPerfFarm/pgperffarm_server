from machines.models import Machine
from machines.serializers import MachineSerializer, MyMachineSerializer, MachineUserSerializer

from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
import hashlib
from django.contrib.auth.hashers import make_password


class AddMachineViewSet(viewsets.ModelViewSet):

	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = MachineSerializer
	lookup_field = 'alias'
	queryset =  Machine.objects.all().order_by('add_time')


	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


	def create(self, request, *args, **kwargs):

		m = hashlib.md5()
		m.update(make_password(str(self.request.data), 'pg_perf_farm').encode('utf-8'))
		machine_secret = m.hexdigest()

		serializer = MachineSerializer(data=self.request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(
			owner_id=self.request.user, 
			machine_secret=machine_secret,
			approved=False
			)

		headers = self.get_success_headers(serializer.data)

		return Response('Machine added successfully!', status=status.HTTP_201_CREATED, headers=headers)


class MachineViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
	List all machines
	"""
	queryset =  Machine.objects.all().order_by('add_time')
	serializer_class = MachineSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class MyMachineViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = MyMachineSerializer
	lookup_field = 'alias'

	
	def get_queryset(self):
		return Machine.objects.filter(owner_id=self.request.user.id).order_by('add_time')


class MachineUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""

	serializer_class = MachineUserSerializer
	queryset = User.objects.all().order_by('email')
	lookup_field = ('username')
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
