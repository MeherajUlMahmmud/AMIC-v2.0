from django.contrib import admin
from .models import CovidTestModel


class CovidTestAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name",
        "gender",
        "status",
        "date",
        "created_at",
    )
    list_filter = ("status", "date")
    search_fields = ("patient_name",)
    list_per_page = 30
    ordering = ("-created_at",)


admin.site.register(CovidTestModel, CovidTestAdmin)
