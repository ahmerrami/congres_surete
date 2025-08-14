from django.urls import path
from .views import hotel_list, hotel_detail
app_name = "hotels"
urlpatterns = [
    path("", hotel_list, name="list"),
    path("<int:pk>/", hotel_detail, name="detail"),
]
