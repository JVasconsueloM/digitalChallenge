from digital_challenge.settings import *
import dj_database_url

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

ENVIRONMENT = 'production'
DEBUG = False
ALLOWED_HOSTS = ['*']
DATABASES['default'] = dj_database_url.config(
    default='DATABASE_URL_HERE'
)