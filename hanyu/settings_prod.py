from hanyu.settings_base import *
import os


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

ALLOWED_HOSTS = ["54.69.87.237",]
