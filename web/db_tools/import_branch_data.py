import sys
import os
from pgperffarm.settings import PORJECT_PATH
# Use django's model independently
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)
path = PORJECT_PATH
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Initialize django
import django
django.setup()

from test_records.models import TestBranch
from data.branch_data import row_data

for branch_item in row_data:
    branch = TestBranch()
    branch.branch_name = branch_item["branch_name"]
    branch.save()