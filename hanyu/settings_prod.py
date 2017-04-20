'''
This module contains the production specific settings.
'''

import os
from hanyu.settings_base import *

ALLOWED_HOSTS = ['*',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hanyu_db',
        'USER': 'hanyu',
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': 'hanyudb.cfxzwnhnvnok.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
