from .base import *

# Password validation
AUTH_PASSWORD_VALIDATORS = []

# Avoid Werkzeug high cpu usage on idle
RUNSERVERPLUS_POLLER_RELOADER_INTERVAL = 5

INSTALLED_APPS = INSTALLED_APPS + ["drf_spectacular"]

SPECTACULAR_SETTINGS = {
    "TITLE": "SmartWareHome API",
    "DESCRIPTION": "",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "COMPONENT_SPLIT_REQUEST": True,
}
