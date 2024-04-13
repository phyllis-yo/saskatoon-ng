"""
Django settings for saskatoon project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/

``django-dotenv`` is used to load environment variables from the
``saskatoon/.env`` file. Please check INSTALL.md for more details.
"""

import os
from pathlib import Path
from dotenv import read_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the environment variables from .env file.
dotenv = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv):
    read_dotenv(dotenv=dotenv)
else:
    raise IOError('.env file not found!')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SASKATOON_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('SASKATOON_DEBUG') is not None:
    DEBUG = os.getenv('SASKATOON_DEBUG', '').lower() in ['yes', 'true']
else:
    DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-ALLOWED_HOSTS

SERVER_IP = os.getenv('SASKATOON_SERVER_IP', '')
if SERVER_IP:
    ALLOWED_HOSTS.append(SERVER_IP)
DOMAIN_NAME = os.getenv('SASKATOON_DOMAIN_NAME', '')
if DOMAIN_NAME:
    ALLOWED_HOSTS.append(DOMAIN_NAME)
#print("ALLOWED_HOSTS", ALLOWED_HOSTS)

# needed by debug toolbar
INTERNAL_IPS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leaflet',
    'sitebase',
    'member',
    'harvest',
    'rest_framework',
    'django_filters',
    'crispy_forms',
    'crispy_bootstrap4',
    'debug_toolbar',
    'django_extensions',
    'django_quill',
    'rosetta',
    'phone_field'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# URLs
ROOT_URLCONF = 'saskatoon.urls'
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

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

WSGI_APPLICATION = 'saskatoon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('SASKATOON_DB_ENGINE'),
        'NAME': os.getenv('SASKATOON_DB_NAME'),
        'USER': os.getenv('SASKATOON_DB_USER'),
        'PASSWORD': os.getenv('SASKATOON_DB_PASSWORD'),
        'HOST': os.getenv('SASKATOON_DB_HOST'),
    }
}

# Remove WARNINGS due to changes in Django3.2 where the type for primary keys can
# now be customized (set by default to BigAutoField starting in Django 3.2):
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('fr',u'Français'),
    ('en',u'English'),
]

ROSETTA_ACCESS_CONTROL_FUNCTION = 'saskatoon.utils.is_translator'

LOCALE_PATHS = [
    'harvest/locale/',
    'member/locale/',
    'sitebase/locale/',
    'saskatoon/locale/'
]

CSRF_COOKIE_SECURE = True

TIME_ZONE = os.getenv('SASKATOON_TIME_ZONE') or 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# user-uploaded files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Statically served PDF files
EQUIPMENT_POINTS_PDF_PATH = os.path.join(MEDIA_ROOT, "guides/equipment_points.pdf")
VOLUNTEER_WAIVER_PDF_PATH = os.path.join(MEDIA_ROOT, "guides/volunteer_waiver.pdf")

# EMAIL SERVER
EMAIL_BACKEND = os.getenv('SASKATOON_EMAIL_BACKEND')
EMAIL_USE_TLS = os.getenv('SASKATOON_EMAIL_USE_TLS')
EMAIL_HOST = os.getenv('SASKATOON_EMAIL_HOST')
EMAIL_PORT = os.getenv('SASKATOON_EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('SASKATOON_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('SASKATOON_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('SASKATOON_EMAIL_FROM')

SEND_MAIL_FAIL_SILENTLY = not EMAIL_HOST
if not EMAIL_BACKEND: del EMAIL_BACKEND

# CUSTOM STUFF

AUTH_USER_MODEL = "member.AuthUser"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
   'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
   'PAGINATE_BY': 10,
   'DEFAULT_RENDERER_CLASSES': (
   'rest_framework.renderers.TemplateHTMLRenderer',
   'rest_framework.renderers.JSONRenderer',
)
}

CACHES = {
    'default': {
        'BACKEND': "django_redis.cache.RedisCache",
        'LOCATION': "redis://127.0.0.1:6379/1",
        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient",
        }
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

CKEDITOR_CONFIGS = {
    'default': {
        'width': "100%"
    },
}

CSRF_FAILURE_VIEW = 'sitebase.views.handler403_csrf_failue'


# LOGS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'brief'
        },
        'file_django': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'when': 'D',  # interval type
            'interval': 1,  # defaults to 1
            'backupCount': 7,  # how many files to keep
            'formatter': 'verbose',
        },
        'file_saskatoon': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/saskatoon.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file_django', 'console'],
            'level': 'WARNING',
            'propogate': True,
        },
        'saskatoon': {
            'handlers': ['file_saskatoon', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
    'formatters': {
        'brief': {
            'format': '{levelname} {asctime} <{name}.{funcName}> {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {name}.{funcName} {process:d} {thread:d} {message}',
            'datefmt': "%d/%b/%Y %H:%M:%S",
            'style': '{',
        }
    }
}

EMAIL_LIST_OUTPUT = os.path.join(BASE_DIR, 'logs/emaillist.csv')
