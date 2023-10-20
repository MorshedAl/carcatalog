"""
WSGI config for carcatalog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import dotenv
from carcatalog import settings

from django.core.wsgi import get_wsgi_application

dotenv.read_dotenv(settings.BASE_DIR / '.env')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carcatalog.settings')

application = get_wsgi_application()