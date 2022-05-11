from django.contrib import admin
from .models import *


class BloodRequestModelAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name",
        "blood_group",
        "quantity",
        "location",
        "is_emergency",
        "is_active",
        "needed_within",
        "phone",
        "created_at",
    )
    list_filter = ["blood_group"]
    search_fields = ["patient_name"]
    list_per_page = 30
    ordering = ["-created_at"]
    raw_id_fields = ["user"]
    date_hierarchy = "created_at"


class PlasmaRequestModelAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name",
        "blood_group",
        "quantity",
        "location",
        "is_emergency",
        "is_active",
        "needed_within",
        "phone",
        "created_at",
    )
    list_filter = ["blood_group"]
    search_fields = ["patient_name"]
    list_per_page = 30
    ordering = ["-created_at"]
    raw_id_fields = ["user"]


class AmbulanceModelAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle_number",
        "city",
        "type",
        "driver_name",
        "driver_phone",
        "driver_email",
        "rent_inter_city",
        "rent_intra_civision",
        "available",
        "created_at",
    )


admin.site.register(BloodRequestModel, BloodRequestModelAdmin)
admin.site.register(PlasmaRequestModel, PlasmaRequestModelAdmin)
admin.site.register(AmbulanceModel, AmbulanceModelAdmin)
