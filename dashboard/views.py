from django.shortcuts import render
from django.http import HttpResponse
from participants.models import Participant
from reservations.models import Reservation
from payments.models import Refund
import csv, io, pandas as pd

def index(request):
    stats = {
        "participants": Participant.objects.count(),
        "reservations": Reservation.objects.count(),
        "paid": Reservation.objects.filter(status=Reservation.Status.PAID).count(),
        "pending": Reservation.objects.filter(status=Reservation.Status.PENDING).count(),
        "cancelled": Reservation.objects.filter(status=Reservation.Status.CANCELLED).count(),
        "refunds": Refund.objects.count(),
    }
    latest = Reservation.objects.select_related("participant","hotel").order_by("-id")[:10]
    return render(request, "dashboard/index.html", {"stats": stats, "latest": latest})

def export_participants_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=participants.csv"
    writer = csv.writer(response)
    writer.writerow(["first_name","last_name","email","phone","nationality","institution","created_at"])
    for p in Participant.objects.all().order_by("last_name"):
        writer.writerow([p.first_name,p.last_name,p.email,p.phone,p.nationality,p.institution,p.created_at])
    return response

def export_reservations_excel(request):
    qs = Reservation.objects.select_related("participant","hotel").all()
    data = [{
        "id": r.id,
        "participant": str(r.participant),
        "email": r.participant.email,
        "hotel": r.hotel.name,
        "room_type": r.room_type,
        "checkin": r.checkin,
        "checkout": r.checkout,
        "nights": r.nights,
        "total_amount": float(r.total_amount),
        "status": r.status
    } for r in qs]
    df = pd.DataFrame(data)
    with io.BytesIO() as output:
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="reservations")
        response = HttpResponse(output.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment; filename=reservations.xlsx"
        return response
