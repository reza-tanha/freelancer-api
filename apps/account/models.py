from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    coin = models.IntegerField(default=0, null=True, blank=True)

    phone = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.email
    