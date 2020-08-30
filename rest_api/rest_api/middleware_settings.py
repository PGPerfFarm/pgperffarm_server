
from django.conf import settings

default_headers = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "origin",
    "user-agent",
    "x-csrftoken",
)

default_methods = ("DELETE", "GET", "PATCH", "POST", "PUT")

class Settings:

	@property
	def CORS_ALLOW_HEADERS(self):
		return default_headers

	@property
	def CORS_ALLOW_METHODS(self):
		return default_methods

middleware_settings = Settings()
