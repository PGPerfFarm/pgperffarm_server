DEBUG = True

DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'pgperffarm',
                'USER': 'ila',
                'PASSWORD': 'password',
                'HOST': '/tmp'
                }
        }

PGAUTH_REDIRECT = ''
PGAUTH_KEY = ''

PROJECT_PATH = '/var/www/web/pgperffarm'
PGAUTH_REDIRECT = ''
PGAUTH_KEY = ''

EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''  # individual smtp password

# PERFFARM_URL = 'http://140.211.168.111:8080/upload/'
PLANT = 'luffa'
SECRET = '0232f37f8e1726684516434441af7454'