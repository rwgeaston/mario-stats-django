# pylint: disable=wildcard-import,unused-wildcard-import

from .settings_components.database import *
from .settings_components.installed_apps import *
from .settings_components.middleware import *
from .settings_components.rest_framework import *

ALLOWED_HOSTS = []

ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

STATIC_URL = '/static/'

try:
    from .local_settings import *  # pylint: disable=wildcard-import,unused-wildcard-import
except ImportError:
    pass
