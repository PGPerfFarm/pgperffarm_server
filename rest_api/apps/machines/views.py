from machines.models import Machine
from machines.serializers import MachineSerializer, MachineHistoryRecordSerializer
from rest_framework import permissions, renderers, viewsets, mixins
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


class MachineHistoryRecordViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Machine info page
    """
    lookup_field = 'sn'
    queryset = Machine.objects.all().order_by('added')
    serializer_class = MachineHistoryRecordSerializer