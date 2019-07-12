from django.contrib.auth.models import User
from rest_framework import viewsets
from users.serializers import UserSerializer
from django.contrib.auth.backends import ModelBackend


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
