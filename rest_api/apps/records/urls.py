from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from records import views

router = DefaultRouter()
router.register(r'all-records', views.TestRecordListViewSet, base_name="records"),
router.register(r'records', views.TestRecordDetailViewSet, base_name="record-detail"),
router.register(r'branches', views.TestBranchListViewSet, base_name="branches"),
router.register(r'category', views.TestCategoryViewSet, base_name="test-category"),
router.register(r'records-by-branch', views.TestRecordListByBranchViewSet, base_name="records-by-branch"),
router.register(r'machine-records', views.MachineHistoryRecordViewSet, base_name="machine-records")

urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'upload/$', views.TestRecordCreate, name="test-upload")
]