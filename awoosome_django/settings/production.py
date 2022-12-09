from .base import *

import django_heroku
import dj_database_url
# from decouple import config

DEBUG = True

ALLOWED_HOSTS = ['*']

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

# INSTALLED_APPS += [
#     'djangoheroku',
#     'dj-database-url',
#     'decouple',
#     'gunicorn',
# ]

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# mail config
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST", "")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", '')
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", "")

django_heroku.settings(locals())