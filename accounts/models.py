from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # linked info can be extended here; keep username/email behavior default but require email unique
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_full_name() or self.username} <{self.email}>"
