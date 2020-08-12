DEBUG = True

DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'pgperffarm',
                'USER': 'ila',
                #'PASSWORD': 'password',
                #'HOST': '/var/run/postgresql',
                'HOST': '/tmp',
                'ATOMIC_REQUESTS': True
                }
        }

PROJECT_PATH = '/var/www/rest_api/'
PGAUTH_REDIRECT = 'http://127.0.0.1:9000/account/auth/1/'
PGAUTH_REDIRECT_SUCCESS = 'http://127.0.0.1:8080/profile/'
PGAUTH_KEY = 'FArsd3dlH2jTXHH/mr9khCtQIMrMmB2uH2qa7Vr3gKU='

EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''  # individual smtp password

