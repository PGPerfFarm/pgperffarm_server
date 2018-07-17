import sys
import os
from pgperffarm.settings import PORJECT_PATH
# Use django's model independently
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)
path = PORJECT_PATH # path = 'D:\GitSpace\pgperffarm\web\pgperffarm'
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Initialize django
import django
django.setup()

from users.models import Alias
from data.alias_data import row_data

for alias_item in row_data:
    alias = Alias()
    alias.name = alias_item["name"]
    alias.is_used = alias_item["is_used"]
    alias.save()