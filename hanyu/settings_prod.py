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

DEBUG = True

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# Files Paths for the Stanford Segmenter. This is a java library accesed via
# an interface in nltk. 
STFD_SEG_DIR = os.path.join(BASE_DIR,'stanford_segmenter_resources', 'stanford-segmenter-2016-10-31') 
SLF4J = os.path.join(STFD_SEG_DIR, 'slf4j-api.jar')
JAVAHOME = r'/usr/lib/jvm/java-8-oracle/jre/bin/java'
CLASSPATH = SLF4J 

STFORD_SEG_SETTINGS = {
    'path_to_jar': os.path.join(STFD_SEG_DIR, 'stanford-segmenter-3.7.0.jar'),
    'path_to_slf4j': os.path.join(STFD_SEG_DIR, 'slf4j-api.jar'),
    'path_to_sihan_corpora_dict': os.path.join(STFD_SEG_DIR, 'data'),
    'path_to_model': os.path.join(STFD_SEG_DIR, 'data', 'pku.gz'),
    'path_to_dict': os.path.join(STFD_SEG_DIR, 'data', 'dict-chris6.ser.gz'),
}




