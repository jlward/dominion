from django.conf import settings
from django.db import models


class Player(models.Model):
    handle = models.CharField(max_length=20)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.handle
