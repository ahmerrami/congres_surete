from django.urls import path
from .views import start, detail, cancel
app_name = "reservations"
urlpatterns = [
    path("start/<int:hotel_id>/", start, name="start"),
    path("<int:res_id>/", detail, name="detail"),
    path("<int:res_id>/cancel/", cancel, name="cancel"),
]
