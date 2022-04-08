from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class UserModelAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_admin', 'is_doctor', 'is_patient', 'last_login')
    search_fields = ('email', 'name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    ordering = ('email',)
    fieldsets = ()
    list_filter = ('is_admin', 'is_active', 'is_doctor', 'is_patient')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


admin.site.register(UserModel, UserModelAdmin)
admin.site.register(DoctorModel, DoctorAdmin)
admin.site.register(PatientModel, PatientAdmin)
admin.site.register(SpecializationModel)
admin.site.register(FeedbackModel)
