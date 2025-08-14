from django.db import models
from reservations.models import Reservation

class Payment(models.Model):
    class Status(models.TextChoices):
        INITIATED = "Initiated"
        SUCCESS = "Success"
        FAILED = "Failed"

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="MAD")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.INITIATED)
    gateway = models.CharField(max_length=20, default="CMI")
    reference = models.CharField(max_length=64, unique=True)
    raw_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Refund(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending"
        SUCCESS = "Success"
        FAILED = "Failed"
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="refunds")
    percent = models.PositiveIntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
