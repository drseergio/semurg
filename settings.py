# -*- coding: utf-8 -*-
from djcelery import setup_loader
from os.path import dirname
from os.path import join
from os.path import realpath
from sys import argv

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = realpath(dirname(__file__))

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'djcelery',
    'indexer',
    'paging',
    'sentry',
    'sentry.client'
)

INSTALLED_APPS += (
    'api',       # REST API layer
    'core',      # business application logic
    'gullwing'   # trading stratagem
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
        'NAME': 'semurg',
        'USER': 'semurg',
        'PASSWORD': 'dN35WShJt7YcVPwf',
        'HOST': '/var/run/mysqld/mysqld.sock',
    }
}
if 'test' in argv:
  DATABASES['default'] = {'ENGINE': 'sqlite3'}

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

CELERY_IMPORTS = ('core.tasks', 'gullwing.tasks', 'core.logic.seeesvee')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SENTRY_PUBLIC = True
SENTRY_TESTING = True

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'api.middleware.NotFound',
)

TEMPLATE_LOADERS = (
   'django.template.loaders.filesystem.Loader',
   'django.template.loaders.app_directories.Loader',
   'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

TIME_ZONE = 'Europe/Zurich'
SECRET_KEY = '8$bps)(y4n#h)8u$udoc-ddt%1-%t=x6-o265gg6@t4v3e*&v2'

ROOT_URLCONF = 'urls'
MEDIA_URL = '/files/'
STATIC_URL = '/static/'
TEMPLATE_DIRS = (join(dirname(__file__), 'templates'),)

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/semurg-emails'

# semurg configuration
VERSION = '0.2.8'
ACCOUNT_CURRENCY = 'CHF'
INSTRUMENT_CURRENCY = 'USD'
MAX_TRANSACTIONS_PER_PAGE = 25
MAX_IMPORT_SIZE = 100 * 1024  # 100 KB
PRICE_URL = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=pol1x'
UPDATE_TIMEOUT = 600
ORDER_SIZE = 10000
EXCHANGE_MAP = {
  'NYSE': 'NYSE',
  'NGM': 'NASDAQ',
  'NasdaqNM': 'NASDAQ',
  'AMEX': 'NYSEAMEX',
  'PCX': 'NYSEARCA' }
# gullwing screener configuration
GULLWING_VERSION = '0.1.0'
SCREENER_URL = ('http://www.google.com/finance?start=0&num=4000&q=%5B('
    '(exchange%20%3D%3D%20%22NYSEARCA%22)%20%7C%20'
    '(exchange%20%3D%3D%20%22NYSEAMEX%22)%20%7C%20'
    '(exchange%20%3D%3D%20%22NYSE%22)%20%7C%20'
    '(exchange%20%3D%3D%20%22NASDAQ%22))%20%26%20'
    '(market_cap%20%3E%3D%20516750000)%20%26%20'
    '(market_cap%20%3C%3D%20420180000000)'
    '%5D&restype=company&output=json&noIL=1&')
# gullwing quotes configuration
QUOTES_URL = 'http://ichart.finance.yahoo.com/table.csv?s=%s'
DAYS_TO_FETCH = 120
# gullwing engine configuration
ENGINE_PATH = realpath(join(dirname(__file__), 'gullwing', 'R', 'engine.R'))
EXTERN_PATH = realpath(join(dirname(__file__), 'gullwing', 'R', 'exterior.R'))
R_DB_CONFIG_PATH = realpath(join(dirname(__file__), 'gullwing', 'R', 'db.yaml'))
R_PATH = '/usr/bin/Rscript'
RUN_HOUR = 22
RUN_MINUTES = [5, 25, 45]  # run 3 times
MAX_HOLD_DAYS = 180
PROFIT_TARGET = 0.4
# analytics configuration
ANALYTICS_SOURCE = 'semurg-semurg-alpha'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'class': 'sentry.client.handlers.SentryHandler'
        }
    },
    'loggers': {
        'core': {
            'handlers': ['sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'logic': {
            'handlers': ['sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'gullwing': {
            'handlers': ['sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api': {
            'handlers': ['sentry'],
            'level': 'DEBUG',
            'propagate': True,
        }
   }
}

try:
  from local_settings import *
except ImportError:
  pass
