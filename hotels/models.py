from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="hotels/", blank=True, null=True)
    single_price = models.DecimalField(max_digits=9, decimal_places=2)
    double_price = models.DecimalField(max_digits=9, decimal_places=2)
    suite_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    quota_single = models.PositiveIntegerField(default=0)
    quota_double = models.PositiveIntegerField(default=0)
    quota_suite = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def has_stock(self, room_type: str) -> bool:
        if room_type == "SINGLE":
            return self.quota_single > 0
        if room_type == "DOUBLE":
            return self.quota_double > 0
        if room_type == "SUITE":
            return self.quota_suite > 0
        return False

    def decrement_stock(self, room_type: str):
        """Decrease stock for the given room type"""
        if room_type == "SINGLE" and self.quota_single > 0:
            self.quota_single -= 1
        elif room_type == "DOUBLE" and self.quota_double > 0:
            self.quota_double -= 1
        elif room_type == "SUITE" and self.quota_suite > 0:
            self.quota_suite -= 1
        else:
            raise ValueError("Insufficient stock for this room type")
        self.save()

    def increment_stock(self, room_type: str):
        """Increase stock for the given room type"""
        if room_type == "SINGLE":
            self.quota_single += 1
        elif room_type == "DOUBLE":
            self.quota_double += 1
        elif room_type == "SUITE":
            self.quota_suite += 1
        else:
            raise ValueError("Unknown room type")
        self.save()