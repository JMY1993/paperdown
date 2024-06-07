from django.db import models

from django.db import models


class Authcode(models.Model):
    serial = models.CharField(max_length=200, unique=True)
    expiration_date = models.DateTimeField()
