from serializer import JWTUserProfileSerializer

# user jwt handler
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': JWTUserProfileSerializer(user).data['username'],
        'status': 1
    }