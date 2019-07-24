import django
import sys
import os

path = '/Users/ila/Desktop/codes/GSoC/pgperffarm/rest_api/rest_api'
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

#from users.models import Alias
from data.alias_data import row_data
from records.models import TestBranch
from data.branch_data import row_data
from records.models import TestCategory
from data.category_data import row_data
from django.contrib.auth.hashers import make_password

django.setup()

'''
for alias_item in row_data:
	alias = Alias()
	alias.name = alias_item["name"]
	alias.is_used = alias_item["is_used"]
	alias.save()
'''

for branch_item in row_data:
	branch = TestBranch()
	branch.branch_name = branch_item["branch_name"]
	# branch.is_accept = True
	# branch.is_show = True
	branch.save()

for test_cate in row_data:
	cate = TestCategory()
	cate.cate_name = test_cate["cate_name"]
	cate.cate_order = test_cate["cate_order"]
	cate.cate_sn = test_cate["cate_sn"]
	cate.save()

