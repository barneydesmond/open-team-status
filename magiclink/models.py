import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from hashids import Hashids


hashids = Hashids(salt=settings.SECRET_KEY)


class MagicToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    ttl = models.IntegerField(default=24, help_text='Time-to-live in hours')

    @property
    def magictoken(self):
        return hashids.encode(self.id, self.user.id, self.ttl)

    @property
    def valid(self):
        expires_at = self.created + datetime.timedelta(hours=self.ttl)
        return expires_at > timezone.now()

    def __str__(self):
        return "{}:{}".format(self.user, self.magictoken)
