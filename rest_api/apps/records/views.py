from django.shortcuts import render
import shortuuid
# from rest_framework_jwt import JSONWebTokenAuthentication, IsAuthenticated

# Create your views here.

@api_view(['POST'])
@permission_classes((UserMachinePermission, ))
def CreateRecord(request, format=None):
    """
    Receive data from client
    """
    print(request.__str__())
    data = request.data

    print(type(data[0]))
    json_data = json.dumps(data[0], encoding="UTF-8", ensure_ascii=False)
    json_data = json.loads(json_data, encoding="UTF-8")

    