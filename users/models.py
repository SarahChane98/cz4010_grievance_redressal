from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_authority = models.BooleanField(default=False)
    pub_key = models.TextField(default='')
    pri_key = models.BinaryField(default=b'')

    def __str__(self):
        return self.username

