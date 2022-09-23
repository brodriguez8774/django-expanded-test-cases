
# System Imports.
import os

# Third-Party Imports.
import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
django.setup()


application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  # Just HTTP for now. (We can add other protocols later.)
})
