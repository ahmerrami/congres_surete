from django.contrib import admin
from .models import Hotel

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name","location","single_price","double_price","suite_price","quota_single","quota_double","quota_suite","active")
    search_fields = ("name","location")
    list_filter = ("active",)
