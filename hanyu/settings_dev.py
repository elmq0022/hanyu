'''
This module contains the development specific settings.
'''

import os
from hanyu.settings_base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hanyu_db',
        'USER': 'hanyu',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '91oqzf9f0(*vkge+t65359da_jdl^fdqv)*g8_edjaqdr83nk&'
