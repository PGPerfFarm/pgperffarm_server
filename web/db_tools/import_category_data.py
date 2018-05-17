import sys
import os

# Use django's model independently
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+ "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PerfFarm.settings")

# Initialize django
import django
django.setup()

# todo