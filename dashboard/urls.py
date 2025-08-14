from django.urls import path
from .views import index, export_participants_csv, export_reservations_excel
app_name = "dashboard"
urlpatterns = [
    path("", index, name="index"),
    path("export/participants.csv", export_participants_csv, name="export_participants_csv"),
    path("export/reservations.xlsx", export_reservations_excel, name="export_reservations_excel"),
]
