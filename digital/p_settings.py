from digital.settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/home/polar/webapps/recursos/digital/static/'
STATIC_URL = '/static/'

MEDIA_ROOT = '/home/polar/webapps/recursos/digital/media/'
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'digital',
        'USER': 'digital',
        'PASSWORD': 'Ericelis21',
        'HOST': 'localhost'
    }
}
