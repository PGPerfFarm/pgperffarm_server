"""rest_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

# packages
from django.conf.urls import url, include
from django.contrib import admin
#from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt import views as jwt_views


# $ curl -X POST -H "Content-Type: application/json" -d '{"username":"<your_username>","password":"<your_password>"}' http://<your_domain_and_port>/auth/

# $ curl -X POST -H "Content-Type: application/json" -d '{"token":"<EXISTING_TOKEN>"}' http://<your_domain_and_port>/auth/refresh_token/

API_TITLE = 'Postgres Performance Farm API'
API_DESCRIPTION = 'A Web API for managing Performance Farm test results.'
schema_view = get_schema_view(title=API_TITLE)

router = routers.DefaultRouter()

urlpatterns = [
    url('', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url('login_token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('refresh_token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url('', include('machines.urls')),
    url('', include('users.urls')),
    url('', include('records.urls')),
    url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    url(r'^schema/$', schema_view),
]
