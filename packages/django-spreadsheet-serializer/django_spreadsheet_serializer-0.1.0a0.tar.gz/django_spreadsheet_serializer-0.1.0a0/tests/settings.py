import os

# Security

SECRET_KEY = "django-insecure-SECRET_KEY"

ALLOWED_HOSTS = ["*"]


# Apps

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "spreadsheet_serializer",
    "tests",
]


# Middleware

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]


# Authentication

AUTH_USER_MODEL = "tests.User"


# Databases

DATABASES = {
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

DATABASES["default"] = DATABASES[os.environ.get("DJANGO_DATABASE", "sqlite")]


# Default autofield

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
