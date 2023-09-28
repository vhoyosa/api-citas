"""
WSGI config for proyecto_citas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

# Set the default settings, and get current environment
from io import BytesIO
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
environment = os.environ.get("DJANGO_SETTINGS_MODULE").split('.')[-1]

if environment not in ['staging', 'production']:
    environment = 'development'

# Initialize the NewRelic agent
newrelic_config = os.environ.get("NEW_RELIC_CONFIG_FILE", 'config/newrelic.ini')

import newrelic.agent
newrelic.agent.initialize(newrelic_config, environment)

# Wrap the WSGI app into with NewRelic
from django.core.wsgi import get_wsgi_application
django_application = newrelic.agent.WSGIApplicationWrapper(get_wsgi_application())

def application(environ, start_response):

    if "chunked" in environ.get("HTTP_TRANSFER_ENCODING", "").lower():
        stream = environ["wsgi.input"]
        data = stream.read()
        environ["CONTENT_LENGTH"] = str(len(data))
        environ["wsgi.input"] = BytesIO(data)

    return django_application(environ, start_response)
