from django.contrib import admin
from .models import Participant

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email","phone","institution","is_confirmed","created_at")
    search_fields = ("first_name","last_name","email","institution")
    list_filter = ("is_confirmed",)
