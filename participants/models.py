from django.db import models

class Participant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=150, blank=True)
    is_confirmed = models.BooleanField(default=False)  # simplifié: confirmé par défaut (email réel à implémenter)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
