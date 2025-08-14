from django.urls import path
from .views import start_payment, cmi_return, cmi_callback, success, failed
app_name = "payments"
urlpatterns = [
    path("start/<int:res_id>/", start_payment, name="start"),
    path("cmi/return/", cmi_return, name="cmi_return"),
    path("cmi/callback/", cmi_callback, name="cmi_callback"),
    path("success/<int:res_id>/", success, name="success"),
    path("failed/<int:res_id>/", failed, name="failed"),
]
