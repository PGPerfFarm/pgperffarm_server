# -*- coding: utf-8 -*-
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema
from .models import UserMachine


class MachineAuthToken(ObtainAuthToken):
    # super.schema
    # super.schema = ManualSchema(
    #     fields=[
    #         coreapi.Field(
    #             name="machine",
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 title="MachineSNS",
    #                 description="Valid MachineSNS for authentication",
    #             ),
    #         ),
    #     ],
    #     encoding="application/json",
    # )

    def post(self, request, *args, **kwargs):
        print(self.schema)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        UserMachine = serializer.validated_data['UserMachine']
        token, created = Token.objects.get_or_create(UserMachine=UserMachine)
        return Response({
            'token': token.key,
            'machine_id': UserMachine,
        })
