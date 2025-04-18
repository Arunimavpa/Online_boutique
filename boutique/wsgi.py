"""
WSGI config for boutique project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""


import os
from django.core.wsgi import get_wsgi_application

# this was still pointing at the example
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_application.settings')
# point at your real settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique.settings')

application = get_wsgi_application()
