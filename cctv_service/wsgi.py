"""
WSGI config for cctv_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

path = '/home/icomputeruser7/cctv_service'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cctv_service.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()