from typing import Any
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from common.utils import info
import environ


env = environ.Env(
)
environ.Env.read_env(settings.BASE_DIR / '.env')
ADMIN_USERNAME = env.str('ADMIN_USERNAME',default='root')
ADMIN_EMAIL = env.str('ADMIN_EMAIL', default='root@mail.com')
ADMIN_PASSWORD = env.str('ADMIN_PASSWORD', default='root')

User = get_user_model()

class Command(BaseCommand):
    
    _class=User
    name='SuperUser'

    @info
    def handle(self, *args: Any, **options: Any) -> str | None:
        self._class.objects.create_superuser(
                ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
        )