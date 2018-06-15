import sys
import os

# Use django's model independently
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+ "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pgperffarm.settings")

# Initialize django
import django
django.setup()

from apps.users.models import Alias
from data.alias_data import row_data

for alias_item in row_data:
    alias = Alias()
    alias.name = alias_item["name"]
    alias.is_used = alias_item["is_used"]
    alias.save()