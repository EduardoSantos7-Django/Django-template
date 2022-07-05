import os
from pathlib import Path

import dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.load_dotenv(BASE_DIR / '..' / '.env')

# Swagger docs settings
# https://drf-spectacular.readthedocs.io/en/latest/settings.html

SPECTACULAR_SETTINGS = {
    'SWAGGER_UI_FAVICON_HREF': '127.0.0.1/favicon.ico',
    'TITLE': "Title",
    'DESCRIPTION': "Description",
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SORT_OPERATIONS': False,
    'SORT_OPERATION_PARAMETERS': False,
}


# Quick-start development settings
# FIXME: https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', '1') == '1'

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,0.0.0.0,localhost").split(",")

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

SECURE_SSL_REDIRECT = not DEBUG

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG

# Application definition

CUSTOM_APPS = [
    'accounts.apps.AccountsConfig',
    'utils',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'rest_framework',
] + CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'admin.urls'

LOGIN_URL = 'sign-in'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'admin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('PG_NAME'),
            'USER': os.getenv('PG_USERNAME'),
            'PASSWORD': os.getenv('PG_PASSWORD'),
            'HOST': os.getenv('PG_HOST'),
            'PORT': os.getenv('PG_PORT'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Email
# https://docs.djangoproject.com/en/4.0/topics/email/

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = os.getenv('EMAIL_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')

EMAIL_USE_TLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'static' / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication
# https://docs.djangoproject.com/en/4.0/topics/auth/customizing/

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']

# DRF
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
