import os

import django

from dj_asgi_utils.core.handlers import ASGIHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def get_asgi_application():
    django.setup(set_prefix=False)
    return ASGIHandler()


application = get_asgi_application()
