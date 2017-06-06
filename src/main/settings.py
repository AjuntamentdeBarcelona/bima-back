# -*- coding: utf-8 -*-

from configurations import Configuration
from django.contrib.messages import constants as messages
from django.utils.translation import ugettext_lazy as _
from kaio import Options
from kaio.mixins import (CachesMixin, DatabasesMixin, CompressMixin, LogsMixin, PathsMixin, SecurityMixin, DebugMixin,
                         WhiteNoiseMixin)
from os.path import join
from bima_back import constants


opts = Options()


class Base(CachesMixin, DatabasesMixin, CompressMixin, PathsMixin, LogsMixin,
           SecurityMixin, DebugMixin, WhiteNoiseMixin, Configuration):
    """
    Project settings for development and production.
    """

    DEBUG = opts.get('DEBUG', True)

    BASE_DIR = opts.get('APP_ROOT', None)
    APP_SLUG = opts.get('APP_SLUG', 'bima-back')
    SITE_ID = 1
    SECRET_KEY = opts.get('SECRET_KEY', 'key')

    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    TIME_ZONE = 'Europe/Madrid'

    ROOT_URLCONF = 'main.urls'
    WSGI_APPLICATION = 'main.wsgi.application'

    INSTALLED_APPS = [

        # django
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # apps
        'main',

        # 3rd parties
        'compressor',
        'constance',
        'constance.backends.database',
        'django_extensions',
        'kaio',
        'robots',
        'widget_tweaks',
        'django_select2',
        'chunked_upload',
        'django_rq',
        'geoposition',
        'django_bootstrap_breadcrumbs',
        'bootstrap_pagination',

        # bima back
        'bima_back',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'main.middleware.force_default_language_middleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    AUTHENTICATION_BACKENDS = [
        'bima_back.authenticate.WSAuthenticationBackend'
    ]

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"

    LOGIN_URL = 'login'
    LOGOUT_REDIRECT_URL = 'login'

    AUTH_USER_MODEL = 'bima_back.DAMUser'

    LANGUAGE_CODE = 'en'
    LANGUAGES = [
        ['en', 'English'],
        ['es', 'Español'],
        ['ca', 'Català'],
    ]
    INTERFACE_LANGUAGE_CODE = LANGUAGE_CODE
    LANGUAGE_SEARCH_FORM_TAGS = constants.LANGUAGE_SEARCH_FORM_TAGS_EN

    # SecurityMiddleware options
    SECURE_BROWSER_XSS_FILTER = True

    COMPRESS_CSS_HASHING_METHOD = "content"

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                # insert additional TEMPLATE_DIRS here
            ],
            'OPTIONS': {
                'context_processors': [
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.tz",
                    'django.template.context_processors.request',
                    'constance.context_processors.config',
                ],
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]
            },
        },
    ]
    if not DEBUG:
        TEMPLATES[0]['OPTIONS']['loaders'] = [
            ('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders']),
        ]

    # Email
    EMAIL_BACKEND = 'django_yubin.smtp_queue.EmailBackend'
    DEFAULT_FROM_EMAIL = opts.get('DEFAULT_FROM_EMAIL', 'Example <info@example.com>')
    MAILER_LOCK_PATH = join(BASE_DIR, 'send_mail')

    # Bootstrap 3 alerts integration with Django messages
    MESSAGE_TAGS = {
        messages.ERROR: 'danger',
    }

    # Constance
    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
    CONSTANCE_DATABASE_CACHE_BACKEND = 'default'
    CONSTANCE_CONFIG = dict(constants.DEFAULT_CONSTANCE)

    # Caches
    CACHE_ENABLED = opts.get('CACHE_ENABLED', True)

    # Constants
    WS_BASE_URL = opts.get('WS_BASE_URL', 'http://127.0.0.1:8000/')

    # Flickr
    FLICKR_ENABLED = opts.get('FLICKR_ENABLED', False)

    # geoposition
    GEOPOSITION_GOOGLE_MAPS_API_KEY = opts.get('GOOGLE_MAPS_API_KEY', 'change_me')
    GEOPOSITION_MAP_OPTIONS = {
        'scrollwheel': True,
        'center': {'lat': 41.4233, 'lng': 2.07289},
        'zoom': 12,
        'minZoom': 3,
        'maxZoom': 20,
    }
    GEOPOSITION_MARKER_OPTIONS = {
        'cursor': 'move',
        'position': {'lat': 41.386995, 'lng': 2.17005},
    }

    # rq
    JOB_DEFAULT_TIMEOUT = opts.get('JOB_DEFAULT_TIMEOUT', 86400)
    RQ_QUEUES = {
        'back': {
            "HOST": opts.get("DJANGO_RQ_DEFAULT_HOST", "localhost"),
            "PORT": opts.get("DJANGO_RQ_DEFAULT_PORT", 6379),
            "DB": opts.get("DJANGO_RQ_DEFAULT_DB", 0),
            "PASSWORD": opts.get("DJANGO_RQ_DEFAULT_PASS", ""),
            "DEFAULT_TIMEOUT": opts.get("DJANGO_RQ_DEFAULT_TIMEOUT", 500)
        }
    }

    # photo create not required fields
    PHOTO_AUTHOR_REQUIRED = opts.get('PHOTO_AUTHOR_REQUIRED', False)
    PHOTO_COPYRIGHT_REQUIRED = opts.get('PHOTO_COPYRIGHT_REQUIRED', False)
    PHOTO_DATE_REQUIRED = opts.get('PHOTO_DATE_REQUIRED', False)

    # hide download buttons for this files
    THUMBOR_UNSUPPORTED_EXTENSIONS = ['.psd', ]

    # photo types
    PHOTO_TYPES_ENABLED = opts.get('PHOTO_TYPES_ENABLED', True)
    PHOTO_TYPES_NAME = _('Brand')


class Test(Base):
    """
    Project settings for testing.
    """

    def DATABASES(self):
        return self.get_databases(prefix='TEST_')
