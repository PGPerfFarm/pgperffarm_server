import sys
import os

# Use django's model independently
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+ "../")
path = 'D:\GitSpace\pgperffarm\web\pgperffarm'
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Initialize django
import django
django.setup()

from test_records.models import TestCategory
from data.category_data import row_data
from django.contrib.auth.hashers import make_password

for test_cate in row_data:
    cate = TestCategory()
    cate.cate_name = test_cate["cate_name"]
    cate.cate_order = test_cate["cate_order"]
    cate.cate_sn = test_cate["cate_sn"]
    cate.save()