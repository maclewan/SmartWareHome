from .base import *

# Password validation
AUTH_PASSWORD_VALIDATORS = []

# Avoid Werkzeug high cpu usage on idle
RUNSERVERPLUS_POLLER_RELOADER_INTERVAL = 5
