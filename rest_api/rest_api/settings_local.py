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