import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

#from users.models import Alias
from data.alias_data import row_data
from data.branch_data import row_data
from data.category_data import row_data
from django.contrib.auth.hashers import make_password

from records.models import TestCategory
from records.models import TestBranch

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
	branch.save()


for test_cate in row_data:
	cate = TestCategory()
	cate.cate_name = test_cate["cate_name"]
	cate.cate_order = test_cate["cate_order"]
	cate.cate_sn = test_cate["cate_sn"]
	cate.save()

