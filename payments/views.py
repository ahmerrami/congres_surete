import uuid, hmac, hashlib
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from reservations.models import Reservation
from .models import Payment

def _sign(payload: dict, secret: str) -> str:
    msg = "&".join(f"{k}={payload[k]}" for k in sorted(payload.keys()))
    return hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()

def start_payment(request, res_id):
    res = get_object_or_404(Reservation, pk=res_id)
    ref = uuid.uuid4().hex[:12].upper()
    pay, _ = Payment.objects.get_or_create(reservation=res, defaults={"amount": res.total_amount, "reference": ref})
    if settings.CMI["MODE"] == "simulate":
        return redirect(reverse("payments:success", args=[res.id]))
    else:
        payload = {
            "merchant_id": settings.CMI["MERCHANT_ID"],
            "amount": f"{res.total_amount:.2f}",
            "currency": settings.CMI["CURRENCY"],
            "order_id": pay.reference,
            "return_url": settings.CMI["RETURN_URL"],
            "callback_url": settings.CMI["CALLBACK_URL"],
        }
        payload["signature"] = _sign(payload, settings.CMI["SECRET"])
        return render(request, "payments/cmi_redirect.html", {"cmi_url": "https://cmi.live/checkout", "payload": payload})

def cmi_return(request):
    messages.info(request, "Retour de CMI reçu (front).")
    return redirect("/")

def cmi_callback(request):
    return HttpResponse("OK")

def success(request, res_id):
    res = get_object_or_404(Reservation, pk=res_id)
    res.status = Reservation.Status.PAID
    res.save(update_fields=["status"])
    if hasattr(res, "payment"):
        res.payment.status = Payment.Status.SUCCESS
        res.payment.save(update_fields=["status"])
    messages.success(request, "Paiement réussi ! Un email de confirmation vous a été envoyé.")
    return render(request, "payments/success.html", {"res": res})

def failed(request, res_id):
    res = get_object_or_404(Reservation, pk=res_id)
    if hasattr(res, "payment"):
        res.payment.status = Payment.Status.FAILED
        res.payment.save(update_fields=["status"])
    messages.error(request, "Le paiement a échoué.")
    return render(request, "payments/failed.html", {"res": res})
