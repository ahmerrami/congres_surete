from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import HomeView, ProgramView, language_switch, debug_language

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("program/", ProgramView.as_view(), name="program"),
    path("i18n/<str:lang>/", language_switch, name="language_switch"),
    # ==================
    path('debug-language/', debug_language, name='debug_language'),
    #===================
    path("participants/", include("participants.urls")),
    path("accounts/", include("accounts.urls")),
    path("hotels/", include("hotels.urls")),
    path("reservations/", include("reservations.urls")),
    path("payments/", include("payments.urls")),
    path("dashboard/", include("dashboard.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

