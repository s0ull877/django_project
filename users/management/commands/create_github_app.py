import os
from typing import Any
from django.core.management import BaseCommand
from allauth.socialaccount import models, providers
from common.utils import info
from django.db import IntegrityError



CLIENT_ID=os.getenv('GITHUB_CLIENT_ID')
CLIENT_SECRET=os.getenv('GITHUB_CLIENT_SECRET')

class Command(BaseCommand):
    
    _class = models.SocialApp
    name='GITHUB_APP'

    @info
    def handle(self, *args: Any, **options: Any) -> str | None:
        if not self._class.objects.filter(provider_id='1').exists():
            socialapp = self._class.objects.create(
                provider='github',
                provider_id='1',
                name='GitHub',
                client_id=CLIENT_ID,
                secret=CLIENT_SECRET
            )
            socialapp.sites.add(1)
        else:
            raise IntegrityError
