from dotenv import load_dotenv
import os
load_dotenv()

from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '8u923hr45677ujhbvcde4r56789pedasc9ijnjk192e8uwydgvdbhnjkiudwyhdn2j1ie837eyftrsdghsj'
DEBUG = True
ALLOWED_HOSTS = ['1509.ddns.net', 'localhost', '127.0.0.1']

# Application definition -------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_extensions',
    'django_filters',
    'django.contrib.postgres',

    # Local Apps
    'helpers',
    'userprofile',
    'organization',
    'problem',
    'judger',
    'submission',
    'compete',

    ##
    "debug_toolbar",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ##
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

SHOW_TOOLBAR_CALLBACK = 'bkdnoj.settings.show_toolbar_callback'
def show_toolbar_callback(request):
    # return settings.DEBUG and not request.is_ajax()
    return True


ROOT_URLCONF = 'bkdnoj.urls'

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

WSGI_APPLICATION = 'bkdnoj.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
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
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

# Fixture folder
FIXTURE_DIRS = [ os.path.join(BASE_DIR, 'bkdnoj', 'fixture'), ]

# Media files (uploaded)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

FILE_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024*1024
## storing into RAM upto 200Mb, someday the server will crash :)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL=True
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000', 'http://1509.dns.net:3000',
# ]

CSRF_COOKIE_HTTPONLY = False
CSRF_TRUSTED_ORIGINS = ['http://1509.ddns.net:3000', 'http://localhost:3000']

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'helpers.custom_pagination.PageCountPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'helpers.custom_pagination.PageNumberPaginationWithoutCount',
    'PAGE_SIZE': 30,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# SimpleJWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

## Celery -------------------------------------------
CELERY_BROKER_URL = 'redis://localhost:6379'
result_backend = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'

## --------- Site settings
DEFAULT_USER_TIME_ZONE = 'Asia/Ho_Chi_Minh'
DEFAULT_USER_LANGUAGE = 'PY3'

BKDNOJ_PROBLEM_DATA_ROOT=os.path.join(MEDIA_ROOT, 'problem_data')
BKDNOJ_PROBLEM_PDF_ROOT=os.path.join(MEDIA_ROOT, 'problem_pdf')

# Some limit for problem settings
BKDNOJ_PROBLEM_MIN_PROBLEM_POINTS = 0.0
BKDNOJ_PROBLEM_MAX_TIME_LIMIT=20.0 # 20 seconds
BKDNOJ_PROBLEM_MIN_TIME_LIMIT=0.1 # 0.1 second = 100 milliseconds
BKDNOJ_PROBLEM_MAX_MEMORY_LIMIT=1024*1024 # 1024*1024 kB = 1024 MB = 1GB
BKDNOJ_PROBLEM_MIN_MEMORY_LIMIT=64*1024 # 64*1024 KB = 64 MB
BKDNOJ_PROBLEM_MAX_OUTPUT_PREFIX=2**30
BKDNOJ_PROBLEM_MAX_OUTPUT_LIMIT=2**30

# When create problem via upload archive, these settings are used to map files to resources
BKDNOJ_PROBLEM_ACCEPTABLE_STATEMENT_PDF = set(['statement.pdf', 'problem.pdf', 'prob.pdf'])
BKDNOJ_PROBLEM_STATEMENT_PDF_FILENAME   = 'problem.pdf'
BKDNOJ_PROBLEM_DATA_IN_FILE_EXT         = ('.in',  '.input',  '.inp', '.i', )
BKDNOJ_PROBLEM_DATA_ANS_FILE_EXT        = ('.out', '.output', '.ans', '.a', )
BKDNOJ_PROBLEM_ACCEPTABLE_CONFIG_EXT = set(['.ini', '.conf'])

# Limit the length of line in problem.ini config file while create problem via archive upload
BKDNOJ_PROBLEM_CONFIG_TOKEN_LENGTH = 2**16

# Allow user to spam submit upto this many subs
BKDNOJ_SUBMISSION_LIMIT = 5

BKDNOJ_DEFAULT_SUBMISSION_OUTPUT_PREFIX = int(1000)
BKDNOJ_DEFAULT_SUBMISSION_OUTPUT_LIMIT = int(1e7)

# For request content of .in/.out file through server
BKDNOJ_PROBLEM_TESTCASE_PREVIEW_LENGTH = int(100)

# For creating new organization
BKDNOJ_ORG_TREE_MAX_DEPTH = 4

BKDNOJ_DISPLAY_RANKS = (
  ('banned', _('Banned User')),
  ('user', _('Normal User')),
  ('setter', _('Problem Setter')),
  ('staff', _('Staff')),
  ('teacher', _('Teacher')),
  ('admin', _('Admin')),
)

## --------- Points scaling params
## Refer to dmoj.ca/post/103-point-system-rework
DMOJ_PP_STEP = 0.95
DMOJ_PP_ENTRIES = 100
DMOJ_PP_BONUS_FUNCTION = lambda n: 300 * (1 - 0.997 ** n)  # noqa: E731

VNOJ_ORG_PP_STEP = 0.95
VNOJ_ORG_PP_ENTRIES = 100
VNOJ_ORG_PP_SCALE = 1

## --------------------------------------------------
EVENT_DAEMON_USE = False
EVENT_DAEMON_POST = 'ws://localhost:9997/'
EVENT_DAEMON_GET = 'ws://localhost:9996/'
EVENT_DAEMON_POLL = '/channels/'
EVENT_DAEMON_KEY = None
EVENT_DAEMON_AMQP_EXCHANGE = 'bkdnoj-events'
EVENT_DAEMON_SUBMISSION_KEY = '6Sdmkx^%pk@GsifDfXcwX*Y7LRF%RGT8vmFpSxFBT$fwS7trc8raWfN#CSfQuKApx&$B#Gh2L7p%W!Ww'

# -- Judger Bridge
BRIDGED_JUDGE_ADDRESS = [('localhost', 9999)]
BRIDGED_JUDGE_PROXIES = None
BRIDGED_DJANGO_ADDRESS = [('localhost', 9998)]
BRIDGED_DJANGO_CONNECT = None

## --------------------------------------------------
