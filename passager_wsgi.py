import os
import sys

from django.core.asgi import get_asgi_application

# Set up paths and environment variables
sys.path.append(os.path.join(os.getcwd(), 'backend'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin.settings'

application = get_asgi_application()
