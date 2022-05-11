from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class UserModelAdmin(UserAdmin):
    list_display = (
        "email",
        "name",
        "is_admin",
        "is_doctor",
        "is_patient",
        "last_login",
    )
    search_fields = ("email", "name")
    readonly_fields = ("date_joined", "last_login")
    list_per_page = 30
    ordering = ("email",)
    list_filter = ("is_admin", "is_active", "is_doctor", "is_patient")


class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "gender",
        "blood_group",
        "date_of_birth",
        "phone",
        "NID",
        "specialization",
        "created_at",
    )
    search_fields = (
        "user",
        "specialization",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_per_page = 30
    ordering = ("created_at",)


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "gender",
        "height",
        "weight",
        "blood_group",
        "date_of_birth",
        "phone",
        "created_at",
    )
    search_fields = ("user",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_per_page = 30
    ordering = ("created_at",)


class SpecializationModelAdmin(admin.ModelAdmin):
    list_display = (
        "specialization",
        "created_at",
        "updated_at",
    )
    search_fields = ("specialization",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_per_page = 30
    ordering = ("specialization",)
    list_filter = ("specialization",)
    date_hierarchy = "created_at"


admin.site.register(UserModel, UserModelAdmin)
admin.site.register(DoctorModel, DoctorAdmin)
admin.site.register(PatientModel, PatientAdmin)
admin.site.register(SpecializationModel, SpecializationModelAdmin)
admin.site.register(FeedbackModel)
