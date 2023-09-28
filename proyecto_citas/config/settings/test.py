# pylint: disable=W0401,W0614
u"""
Django test settings for proyecto_citas project.
"""

from .base import *

TEST_MODE = True

APP_ENVIRONMENT = 'test'

ALLOWED_HOSTS = [
    'localhost',
    'testserver',
    # the Django HTTP test client performs its requests by default with a
    # SERVER_NAME == testserver ; this causes problems with mercadopago,
    # because when we perform a payment request to their API, they expect
    # from us a "webhook" field, which includes the SERVER_NAME, and the
    # mercadopago API considers https://servername/.... an invalid value, I
    # suspect because it doesn't have any TLD at the end (.org, .com,
    # whatever).
    #
    # This addition here allows the test code to perform requests using
    # testserver.org; the addition is necessary because without it a request
    # in our tests with this particular SERVER_NAME would fail without even
    # reaching our view, with HTTP 400 error.
    'testserver.org',
    'ec2-34-204-78-207.compute-1.amazonaws.com'
]

SECRET_KEY = 'JAJAJAJAJAJAJAJE'

# when testing, use the default database router, since we use only one database
DATABASE_ROUTERS = []

RDS_DB_NAME = 'citas'
if os.environ.get('RDS_DB_NAME'):
    RDS_DB_NAME = os.environ.get('RDS_DB_NAME')

RDS_HOSTNAME = 'db'
if os.environ.get('RDS_HOSTNAME'):
    RDS_HOSTNAME = os.environ.get('RDS_HOSTNAME')

RDS_PORT = '5432'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': RDS_DB_NAME,
        'USER': getenvvar('RDS_USERNAME'),
        'PASSWORD': getenvvar('RDS_PASSWORD'),
        'HOST': RDS_HOSTNAME,
        'PORT': RDS_PORT,
    },
}
