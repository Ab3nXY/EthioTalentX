"""
WSGI config for ethiotalentx project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application
from pathlib import Path

# Define BASE_DIR to reference the project's root directory
BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ethiotalentx.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))