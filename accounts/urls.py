from django.urls import path
from .views import register_view, activate_view, profile_view, MyReservationsView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm

app_name = "accounts"
urlpatterns = [
    path("register/", register_view, name="register"),
    path("activate/<str:token>/", activate_view, name="activate"),
    path("login/", LoginView.as_view(template_name='accounts/login.html', authentication_form=UserLoginForm), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("profile/", profile_view, name="profile"),
    path("mes-reservations/", MyReservationsView.as_view(), name="my_reservations"),
]
