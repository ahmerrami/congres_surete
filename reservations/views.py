import json
import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required

from participants.models import Participant
from hotels.models import Hotel
from .models import Reservation
from payments.models import Payment, Refund


@login_required
def start(request, hotel_id):
    """
    Démarre une réservation pour un hôtel spécifique.
    """
    hotel = get_object_or_404(Hotel, pk=hotel_id, active=True)

    # Récupérer le participant lié à l'utilisateur
    try:
        participant = Participant.objects.get(email=request.user.email)
    except Participant.DoesNotExist:
        messages.error(request, "Votre profil participant est introuvable. Veuillez le compléter.")
        return redirect('accounts:profile')

    # Vérifier si le compte utilisateur est confirmé
    if not getattr(request.user, 'is_confirmed', False):
        messages.error(request, 'Veuillez activer votre compte via l’email reçu avant de réserver.')
        return redirect('accounts:profile')

    from .forms import ReservationForm

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            room_type = form.cleaned_data['room_type']

            # Vérifier le stock sans le décrémenter
            if not hotel.has_stock(room_type):
                messages.error(request, "Plus de stock pour ce type de chambre. Merci de choisir un autre type ou hôtel.")
            else:
                with transaction.atomic():
                    res = form.save(commit=False)
                    res.participant = participant
                    res.hotel = hotel
                    res.nights = res.compute_nights()
                    res.total_amount = res.compute_total()
                    res.save()

                    # Décrémenter le stock en s'assurant qu'il ne devient pas négatif
                    if hotel.has_stock(room_type):
                        hotel.decrement_stock(room_type)
                        hotel.save()
                    else:
                        messages.error(request, "Stock épuisé pendant la transaction. Veuillez réessayer.")
                        return redirect("reservations:start", hotel_id=hotel.id)

                messages.success(request, "Réservation créée. Veuillez procéder au paiement.")
                return redirect("payments:start", res_id=res.id)
    else:
        form = ReservationForm()

    return render(
        request,
        "reservations/start.html",
        {"hotel": hotel, "form": form, "participant": participant}
    )


@login_required
def detail(request, res_id):
    """
    Affiche le détail d'une réservation.
    """
    res = get_object_or_404(Reservation, pk=res_id)
    refund = Refund.objects.filter(payment__reservation=res).first()
    return render(request, "reservations/detail.html", {"res": res, "refund": refund})


@login_required
def cancel(request, res_id):
    """
    Annule une réservation et calcule le remboursement selon REFUND_RULES.
    """
    res = get_object_or_404(Reservation, pk=res_id)

    # Conversion de la date depuis settings
    event_start = getattr(settings, "EVENT_START_DATE", None)
    if isinstance(event_start, datetime.date):
        event_start_date = event_start
    elif isinstance(event_start, str):
        try:
            event_start_date = datetime.datetime.strptime(event_start, "%Y-%m-%d").date()
        except ValueError:
            event_start_date = datetime.date.today()
    else:
        event_start_date = datetime.date.today()

    days_before = (event_start_date - datetime.date.today()).days
    percent = 0
    rules = sorted(settings.REFUND_RULES, key=lambda r: r["min_days"], reverse=True)
    for r in rules:
        if days_before >= int(r["min_days"]):
            percent = int(r["percent"])
            break

    refund_amount = (res.total_amount * percent) / 100 if res.status == Reservation.Status.PAID else 0

    if request.method == "POST":
        with transaction.atomic():
            res.status = Reservation.Status.CANCELLED
            res.save(update_fields=["status"])

            # Ré-incrémenter le stock de la chambre annulée
            if res.hotel and res.room_type:
                res.hotel.increment_stock(res.room_type)
                res.hotel.save()

            if (
                hasattr(res, "payment") and 
                res.payment.status == Payment.Status.SUCCESS and 
                refund_amount > 0
            ):
                # Créer un remboursement (simulation ou live via CMI)
                Refund.objects.create(
                    payment=res.payment,
                    percent=percent,
                    amount=refund_amount,
                    status=Refund.Status.SUCCESS if getattr(settings, "CMI_MODE", "simulate") == "simulate" else Refund.Status.PENDING
                )

                if getattr(settings, "CMI_MODE", "simulate") == "simulate":
                    messages.success(
                        request,
                        f"Annulation confirmée. Remboursement simulé: {percent}% ({refund_amount} MAD)."
                    )
                else:
                    messages.info(request, "Annulation confirmée. Remboursement en cours via CMI.")
            else:
                messages.success(request, "Annulation confirmée.")

        return redirect("reservations:detail", res_id=res.id)

    return render(
        request,
        "reservations/cancel.html",
        {"res": res, "percent": percent, "refund_amount": refund_amount}
    )