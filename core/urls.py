from django.urls import path
from .views import HomeView, ProgramView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("program/", ProgramView.as_view(), name="program"),
]