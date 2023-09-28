# pylint: disable=W0401,W0614
u"""
Django development settings for proyecto_citas project.
"""
import os
from .base import *

DEBUG = True

SECRET_KEY = '(k(l)@ht14-%q3l&hp9^(r8+ao+9jpc-y48cfv8i-5tcqzf@lh'

RDS_DB_NAME = 'citas'
RDS_HOSTNAME = 'db'
RDS_PORT = '5432'

DATABASES['default']['NAME'] = RDS_DB_NAME
DATABASES['default']['HOST'] = RDS_HOSTNAME
DATABASES['default']['PORT'] = RDS_PORT
DATABASES['default']['OPTIONS'] = {'sslmode':'disable'}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

ALLOWED_HOSTS = [
    'localhost',
    'ec2-34-204-78-207.compute-1.amazonaws.com'
]
