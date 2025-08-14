from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from participants.models import Participant
from hotels.models import Hotel

class Reservation(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = "SINGLE", _("Single")
        DOUBLE = "DOUBLE", _("Double")
        SUITE = "SUITE", _("Suite")

    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")
        CANCELLED = "CANCELLED", _("Cancelled")

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="reservations")
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, related_name="reservations")
    room_type = models.CharField(max_length=10, choices=RoomType.choices)
    checkin = models.DateField()
    checkout = models.DateField()
    nights = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Res#{self.id} {self.participant} @ {self.hotel}"

    def compute_nights(self):
        return (self.checkout - self.checkin).days

    def unit_price(self):
        return {
            self.RoomType.SINGLE: self.hotel.single_price,
            self.RoomType.DOUBLE: self.hotel.double_price,
            self.RoomType.SUITE: self.hotel.suite_price,
        }[self.room_type]

    def compute_total(self):
        return self.unit_price() * self.compute_nights()
