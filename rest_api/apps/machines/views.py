from django.shortcuts import render
#from djangorestframework_jwt import JSONWebTokenAuthentication, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from machines.models import Machine
from machines.serializers import MachineSerializer
from rest_framework.parsers import JSONParser

# listing all existing machines or creating a new one

@api_view(['GET', 'POST'])
def machine_list(request, format=None):

	try:
		machine = Machine.objects.get(sn=sn)
	except Machine.DoesNotExist:
   		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = MachineSerializer(machine)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = MachineSerializer(machine, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		machine.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def machine_detail(request, sn):

	try:
		machine = Machine.objects.get(sn=sn)
	except Machine.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = MachineSerializer(machine)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = MachineSerializer(machine, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		machine.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
