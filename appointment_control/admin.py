from django.contrib import admin
from .models import *


class AppointmentModelAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "doctor",
        "department",
        "date",
        "time",
        "is_accepted",
        "is_canceled",
        "is_complete",
        "created_at",
    ]
    list_filter = ["date", "is_accepted", "is_canceled", "is_complete"]
    search_fields = ["patient", "doctor", "department", "date", "time"]
    list_per_page = 10
    ordering = ["-created_at"]


admin.site.register(AppointmentModel, AppointmentModelAdmin)
admin.site.register(PrescriptionModel)
