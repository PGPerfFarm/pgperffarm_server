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

from users.models import UserProfile
from data.user_data import row_data
from django.contrib.auth.hashers import make_password

for user_deatil in row_data:
    users = UserProfile()
    users.password = make_password(user_deatil["password"])
    users.is_superuser = user_deatil["is_superuser"]
    users.username = user_deatil["username"]
    users.email = user_deatil["email"]
    users.is_staff = user_deatil["is_staff"]
    users.is_active = user_deatil["is_active"]

    users.save()