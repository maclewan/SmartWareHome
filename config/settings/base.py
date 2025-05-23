from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

SECRET_KEY = "django-insecure-0r1nb)b1$!t8xmwfqeaw#@z#h94aqet5ru=b5iwo)$&so7o(#e"

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["http://0.0.0.0", "https://supplies.lewandowicz.it"]

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    "rest_framework",
    "django_no_queryset_admin_actions",
]

LOCAL_APPS = [
    "ware_home.users.apps.UsersConfig",
    "ware_home.supplies.apps.SuppliesConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Default user model
AUTH_USER_MODEL = "users.User"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "CET"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = (BASE_DIR / "static",)

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom vars
UPC_DATABASE_API_KEY = config("UPC_DATABASE_API_KEY", default="")

# login url
LOGIN_URL = "/admin/login/"

BASE_DOMAIN = config("BASE_DOMAIN", "")
STICKER_PRINTER_MAC = "0F:1A:C6:62:A8:55"
STICKER_PRINTER_CHANNEL = 1

TARGET_QR_WIDTH = 370
QR_DESCR_HEIGHT = 100
COLUMN_GAP = 20

QR_FONT_PATH = "static/fonts/Roboto-Bold.ttf"
