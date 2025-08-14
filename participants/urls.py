from django.urls import path
from django.urls import include, path
urlpatterns = [ path('', include('accounts.urls')) ]
