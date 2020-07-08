from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, viewsets, generics, views, mixins, authentication, response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import list_route
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from users.serializers import UserSerializer


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""

	serializer_class = UserSerializer
	queryset = User.objects.all().order_by('email')
	lookup_field = ('username')


