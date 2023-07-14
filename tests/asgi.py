
# System Imports.
import os

# Third-Party Imports.
import django
from channels.routing import ProtocolTypeRouter

# Import handling for post-Django V2.
try:
    from django.core.asgi import get_asgi_application as AsgiHandler
    # Success. Is Django3 or higher.
except ImportError:
    # Failure. Likely Django 2.
    from channels.http import AsgiHandler


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
django.setup()


application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  # Just HTTP for now. (We can add other protocols later.)
})
