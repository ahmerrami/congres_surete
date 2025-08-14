from django import forms
from django.conf import settings
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["room_type", "checkin", "checkout"]

    def clean(self):
        cleaned = super().clean()
        checkin = cleaned.get("checkin")
        checkout = cleaned.get("checkout")
        es = settings.EVENT_START_DATE
        ee = settings.EVENT_END_DATE
        if checkin and checkout:
            if not (es <= checkin <= ee) or not (es <= checkout <= ee or checkout == ee):
                raise forms.ValidationError("Les dates doivent être dans la période du congrès.")
            if checkout <= checkin:
                raise forms.ValidationError("La date de départ doit être après la date d'arrivée.")
        return cleaned
