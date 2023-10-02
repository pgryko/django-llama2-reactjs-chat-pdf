"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import logging
from pathlib import Path

import structlog
from decouple import config
from dj_database_url import parse as db_url
import os

from django.urls import reverse_lazy

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from structlog_sentry import SentryProcessor

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# random default generated for testing purposes - make sure to change this in production or local dev
# otherwise session data will be invalidated on every server restart or completely broken if running multiple
# workers
SECRET_KEY = config(
    "SECRET_KEY", "django-insecure-677r0v$n7m-2o2sezi=#ova1ad3eyf^pciz=*8_yh4hb2jt3x&"
)

# SECRET_KEY = config("SECRET_KEY", secrets.token_hex(32))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "accounts.apps.AccountsConfig",
    "chat.apps.ChatConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "server/templates"),
            os.path.join(BASE_DIR, "templates"),
        ],
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

WSGI_APPLICATION = "server.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": config(
        "DATABASE_URL", default=f"sqlite:///{BASE_DIR}/db.sqlite3", cast=db_url
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_ROOT = BASE_DIR / "staticfiles"

CHROMADB_PATH = config("CHROMADB_PATH", ".chromadb")

AUTH_USER_MODEL = "accounts.AccountUser"

REPLICATE_API_TOKEN = config("REPLICATE_API_TOKEN", "")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
# CSRF_COOKIE_AGE = None

ACCESS_TOKEN_EXPIRE_MINUTES = 5

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    "http://127.0.0.1,http://localhost",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

LOGIN_REDIRECT_URL = reverse_lazy("chatroom_list")
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/"

SENTRY_DSN = config("SENTRY_DSN", None)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

HUGGING_FACE_API_TOKEN = config("HUGGING_FACE_API_TOKEN", None)


root_logger = logging.getLogger()
root_logger.setLevel(logging.ERROR)  # or whichever level you desire
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(message)s"))
root_logger.addHandler(console_handler)

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(event_level=None, level=None),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production (e.g. 0.1
        traces_sample_rate=config("SENTRY_TRACES_SAMPLE_RATE", 1.0, cast=float),
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=config("SENTRY_PROFILE_SAMPLE_RATE", 1.0, cast=float),
        environment=os.environ.get("ENV_NAME", "dev"),
    )

    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,  # optional, must be placed before SentryProcessor()
            structlog.stdlib.add_log_level,  # required before SentryProcessor()
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # Add a console renderer here
            structlog.dev.ConsoleRenderer(),
            SentryProcessor(event_level=logging.ERROR),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        cache_logger_on_first_use=True,
    )

else:
    # Log to console only
    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        cache_logger_on_first_use=True,
    )


if DEBUG:
    # Add django extensions
    # Provides additional dev tools such as runserver_plus
    INSTALLED_APPS.append("django_extensions")

    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    # When serving over https
    SECURE_HSTS_SECONDS = 3600
