from django.contrib import admin
from .models import *


class TestTypeModelAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


class TestModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "test_type",
        "status",
        "date",
        "created_at",
    )
    list_filter = ["test_type", "status"]
    search_fields = ["name"]
    list_per_page = 30
    ordering = ["-created_at"]
    raw_id_fields = ["test_type"]
    date_hierarchy = "created_at"


admin.site.register(TestTypeModel, TestTypeModelAdmin)
admin.site.register(TestModel, TestModelAdmin)
