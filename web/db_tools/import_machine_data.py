import sys
import os

# Use django's model independently
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+ "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PerfFarm.settings")

# Initialize django
import django
django.setup()

from apps.user_operation.models import UserMachine
from data.machine_data import row_data
from django.contrib.auth.hashers import make_password

for machine_item in row_data:
    machine = UserMachine()

    machine.machine_sn = machine_item["machine_sn"]
    machine.machine_secret = machine_item["machine_secret"]
    machine.alias = machine_item["alias"]
    machine.os_name = machine_item["os_name"]
    machine.os_version = machine_item["os_version"]
    machine.comp_name = machine_item["comp_name"]
    machine.comp_version = machine_item["comp_version"]
    machine.machine_owner_id = machine_item["machine_owner_id"]

    machine.save()