"""
Django settings for the Blood Bank Management System (BBMS).

Shared file — built across three PRs:
  - Rithish P M (PR #1):  base Django settings, database, middleware
  - Ritesh Kumar Sharma (PR #2):  INSTALLED_APPS entries, AUTH_USER_MODEL, REST_FRAMEWORK
  - Reyansh (PR #3):  PASSWORD_HASHERS (SR-003), SIMPLE_JWT expiry (SR-005)
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Core settings (Rithish P M — PR #1)
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# BBMS-SR-005 / security: secret key read from environment variable
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-dev-key-change-in-production',
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # --- Added by Ritesh Kumar Sharma (PR #2) ---
    'rest_framework',
    'accounts',
    'donations',
    'inventory',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bbms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bbms.wsgi.application'

# Database — SQLite for local dev (zero setup), switchable to PostgreSQL
# via environment variables.  Recorded in docs/DEVIATIONS.md.
DATABASE_ENGINE = os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3')
DATABASE_NAME = os.environ.get('DB_NAME', str(BASE_DIR / 'db.sqlite3'))

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
    }
}

# Add PostgreSQL-specific fields when using that backend
if 'postgresql' in DATABASE_ENGINE:
    DATABASES['default'].update({
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    })

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------------------------------
# Custom user model & REST framework (Ritesh Kumar Sharma — PR #2)
# ---------------------------------------------------------------------------

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
