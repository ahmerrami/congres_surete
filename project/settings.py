from pathlib import Path
import os, json, datetime
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
DEBUG = os.getenv("DJANGO_DEBUG","True").lower() == "true"
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS","").split(",") if h.strip()] or ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Ajoute les providers si besoin, ex: 'allauth.socialaccount.providers.google'

    "crispy_forms",
    "crispy_bootstrap5",
    "accounts",
    "core",
    "participants",
    "hotels",
    "reservations",
    "payments",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "project.wsgi.application"
ASGI_APPLICATION = "project.asgi.application"

DB_ENGINE = os.getenv("DB_ENGINE","sqlite")
if DB_ENGINE == "sqlite":
    DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR / os.getenv("DB_NAME","db.sqlite3")}}
else:
    DATABASES = {"default":{
        "ENGINE":"django.db.backends.postgresql",
        "NAME":os.getenv("DB_NAME","congres"),
        "USER":os.getenv("DB_USER",""),
        "PASSWORD":os.getenv("DB_PASSWORD",""),
        "HOST":os.getenv("DB_HOST","localhost"),
        "PORT":os.getenv("DB_PORT","5432"),
    }}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = os.getenv("DEFAULT_LANGUAGE_CODE","en")
LANGUAGES = [("fr","Français"),("en","English")]
TIME_ZONE = os.getenv("TIME_ZONE","Africa/Casablanca")
USE_I18N = True
USE_TZ = True

#----------------------------------------------

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

#----------------------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND","django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL","no-reply@congres-surete.test")
SITE_URL = os.getenv("SITE_URL","http://127.0.0.1:8000")

ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

CMI = {
    "MODE": os.getenv("CMI_MODE","simulate"),
    "MERCHANT_ID": os.getenv("CMI_MERCHANT_ID",""),
    "SECRET": os.getenv("CMI_SECRET",""),
    "CURRENCY": os.getenv("CMI_CURRENCY","MAD"),
    "RETURN_URL": os.getenv("CMI_RETURN_URL",""),
    "CALLBACK_URL": os.getenv("CMI_CALLBACK_URL",""),
}

EVENT_START_DATE = datetime.date.fromisoformat(os.getenv("EVENT_START_DATE","2025-12-02"))
EVENT_END_DATE = datetime.date.fromisoformat(os.getenv("EVENT_END_DATE","2025-12-04"))
REFUND_RULES = json.loads(os.getenv("REFUND_RULES",'[{"min_days":30,"percent":80},{"min_days":15,"percent":50},{"min_days":0,"percent":0}]'))

AUTH_USER_MODEL = 'accounts.User'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
