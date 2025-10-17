from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-secret-key')

# Read DEBUG from environment (default True for local development)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')

# For deployment on Render, allow the service host explicitly
ALLOWED_HOSTS = ['defesa2-0-rkmo.onrender.com']
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"   # pra onde vai depois de logar
LOGOUT_REDIRECT_URL = "/login/"       # pra onde vai depois de sair


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ocorrencias',
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

ROOT_URLCONF = 'defesacivil_sqlite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Adiciona o diretório de templates
        'APP_DIRS': True,  # Isso permite procurar por templates nas pastas dos apps
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

WSGI_APPLICATION = 'defesacivil_sqlite.wsgi.application'

# Allow configuring the DB via a single DATABASE_URL (Render / Supabase friendly)
# Examples: postgres://user:pass@host:5432/dbname or postgresql://...
_database_url = os.environ.get('DATABASE_URL')
if _database_url:
    # Parse simple DATABASE_URL without adding a new dependency
    # Format: scheme://user:password@host:port/name
    try:
        from urllib.parse import urlparse

        _parsed = urlparse(_database_url)
        _db_name = _parsed.path.lstrip('/') or os.environ.get('DB_NAME', 'postgres')
        _db_user = _parsed.username or os.environ.get('DB_USER', 'postgres')
        _db_password = _parsed.password or os.environ.get('DB_PASSWORD', '')
        _db_host = _parsed.hostname or os.environ.get('DB_HOST', 'localhost')
        _db_port = str(_parsed.port) if _parsed.port else os.environ.get('DB_PORT', '5432')
        _db_sslmode = os.environ.get('DB_SSLMODE', 'require')
    except Exception:
        _db_name = os.environ.get('DB_NAME', 'postgres')
        _db_user = os.environ.get('DB_USER', 'postgres')
        _db_password = os.environ.get('DB_PASSWORD', '')
        _db_host = os.environ.get('DB_HOST', 'localhost')
        _db_port = os.environ.get('DB_PORT', '5432')
        _db_sslmode = os.environ.get('DB_SSLMODE', 'require')
else:
    _db_name = os.environ.get('DB_NAME', 'postgres')
    _db_user = os.environ.get('DB_USER', 'postgres')
    # IMPORTANT: set DB_PASSWORD in environment (do not commit secrets)
    _db_password = os.environ.get('DB_PASSWORD', '')
    _db_host = os.environ.get('DB_HOST', 'aws-1-sa-east-1.pooler.supabase.com')
    _db_port = os.environ.get('DB_PORT', '5432')
    _db_sslmode = os.environ.get('DB_SSLMODE', 'require')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': _db_name,
        'USER': _db_user,
        'PASSWORD': _db_password,
        'HOST': _db_host,
        'PORT': _db_port,
        'OPTIONS': {
            'sslmode': _db_sslmode,
            'client_encoding': 'UTF8',
        }
    }
}

# If no external Postgres configuration is detected and we're in DEBUG mode,
# fall back to a local SQLite DB so the site can run for development/testing
# without a provisioned Supabase/Postgres instance.
_using_sqlite_fallback = False
if DEBUG:
    # Consider falling back if DB_HOST is not set or points to the Supabase default
    if not os.environ.get('DATABASE_URL') and (not os.environ.get('DB_HOST') or os.environ.get('DB_HOST') == 'aws-1-sa-east-1.pooler.supabase.com'):
        _using_sqlite_fallback = True

if _using_sqlite_fallback:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


