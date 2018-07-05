"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token

from rest_framework.authtoken import views
from django.contrib import admin
from django.views.generic.base import RedirectView

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from test_records.views import TestRecordListViewSet, TestRecordCreate, TestRecordDetailViewSet, \
    MachineHistoryRecordViewSet
from test_records.auth import MachineAuthToken
# from test_records.view_base import TestListView

# config test record url
# test_record_list = TestRecordListViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
router = DefaultRouter()
router.register(r'records', TestRecordListViewSet, base_name="records")
router.register(r'detail', TestRecordDetailViewSet, base_name="detail")
router.register(r'machine', MachineHistoryRecordViewSet, base_name="machine")
# router.register(r'detail', TestRecordListViewSet)

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),


    url(r'^api-token-auth/', views.obtain_auth_token),

    # login(jwt auth)
    url(r'^login/', obtain_jwt_token),

    url(r'^machine-token-auth/', MachineAuthToken.as_view()),
    url(r'^', include(router.urls)),
    # url(r'status/$', test_record_list, name='test-list'),
    # url(r'status/$', TestListView.as_view(), name='test-list'),
    # url(r'detail', TestRecordDetailViewSet ,name="detail"),
    url(r'upload/$', TestRecordCreate, name='test-upload'),
    url(r'docs/', include_docs_urls(title='pgperffarm')),
    # Static pages
    # url(r'^$', 'pgperffarm.views.index', name='index'),
    # url(r'^/licence$', 'pgperffarm.views.licence', name='licence'),
    # url(r'^/ppolicy$', 'pgperffarm.views.ppolicy', name='ppolicy'),
    #
    # # Auth system integration
    # url(r'^(?:account/)?login/?$', 'pgperffarm.auth.login'),
    # url(r'^(?:account/)?logout/?$', 'pgperffarm.auth.logout'),
    # url(r'^auth_receive/$', 'pgperffarm.auth.auth_receive'),
    #
    # # Admin site
    # url(r'^admin/', include(admin.site.urls)),
    #
    # # This should not happen in production - serve with lightty!
    # url(r'^static/(.*)$', 'django.views.static.serve', {
    #     'document_root': '/static',
    # }),
]