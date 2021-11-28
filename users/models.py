from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_authority = models.BooleanField(default=False)
    pub_key = models.TextField()
    pri_key = models.TextField()
    nonce = models.TextField()

    def __str__(self):
        return self.username

