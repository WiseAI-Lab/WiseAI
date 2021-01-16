import warnings
from .common import *

DEBUG = True

ALLOWED_HOSTS = ["*"]
AUTH_USER_MODEL = "accounts.UserProfile"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_NAME", "postgres"),  # noqa: ignore=F405
        "USER": os.environ.get(  # noqa: ignore=F405
            "POSTGRES_USER", "postgres"
        ),  # noqa: ignore=F405
        "PASSWORD": os.environ.get(  # noqa: ignore=F405
            "POSTGRES_PASSWORD", "postgres"
        ),  # noqa: ignore=F405
        "HOST": os.environ.get(  # noqa: ignore=F405
            "POSTGRES_HOST", "localhost"
        ),  # noqa: ignore=F405
        "PORT": os.environ.get("POSTGRES_PORT", 5432),  # noqa: ignore=F405
    }
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"

# DJANGO-SPAGHETTI-AND-MEATBALLS SETTINGS
# INSTALLED_APPS += [  # noqa: ignore=F405
#
# ]

# SILKY_PYTHON_PROFILER = True

# Prevents Datetime warning by showing errors
warnings.filterwarnings(
    "error",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r"django\.db\.models\.fields",
)
