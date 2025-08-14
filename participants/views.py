
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import signing, mail
from django.urls import reverse
from django.conf import settings
from .forms import ParticipantForm
from .models import Participant

def _activation_token(email: str) -> str:
    return signing.TimestampSigner().sign(email)

def _activation_link(token: str) -> str:
    return f"{settings.SITE_URL}{reverse('activate', args=[token])}".replace('%2F','/')

def register(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.is_confirmed = False
            p.save()
            # send activation email
            token = _activation_token(p.email)
            link = _activation_link(token)
            subject = "Activation de votre inscription — Congrès Sûreté"
            body = f"Bonjour {p.first_name},\n\nMerci pour votre inscription. Veuillez activer votre compte en cliquant sur le lien suivant :\n{link}\n\nCordialement."
            mail.send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [p.email], fail_silently=False)
            messages.success(request, "Inscription enregistrée. Un email d’activation vous a été envoyé.")
            return redirect("home")
    else:
        form = ParticipantForm()
    return render(request, "participants/register.html", {"form": form})

def activate(request, token: str):
    try:
        email = signing.TimestampSigner().unsign(token, max_age=60*60*24*7)  # 7 jours
        p = Participant.objects.get(email=email)
        if not p.is_confirmed:
            p.is_confirmed = True
            p.save(update_fields=["is_confirmed"])
            messages.success(request, "Votre compte est activé. Vous pouvez réserver votre hôtel.")
        else:
            messages.info(request, "Votre compte est déjà activé.")
    except Exception:
        messages.error(request, "Lien d’activation invalide ou expiré.")
    return redirect("hotels:list")
