from django.db import models


class Player(models.Model):
    handle = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.handle
