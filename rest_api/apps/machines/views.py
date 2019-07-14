from machines.models import Machine
from machines.serializers import MachineSerializer
from rest_framework import permissions, renderers, viewsets
from machines.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse


class MachineViewSet(viewsets.ModelViewSet):

	queryset = Machine.objects.all()
	serializer_class = MachineSerializer
	permission_classes = (
		permissions.IsAuthenticatedOrReadOnly,
		IsOwnerOrReadOnly, 
		)

	'''
	@detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
	def highlight(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)
	  '''

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)