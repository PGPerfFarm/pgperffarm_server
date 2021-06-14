from urllib.parse import urlparse
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
ACCESS_CONTROL_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"


class CorsMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        patch_vary_headers(response, ["Origin"])

        origin = request.META.get("HTTP_ORIGIN")
        if not origin:
            return response

        url = urlparse(origin)

        response[ACCESS_CONTROL_ALLOW_CREDENTIALS] = "true"
        response[ACCESS_CONTROL_ALLOW_ORIGIN] = "*"

        return response
