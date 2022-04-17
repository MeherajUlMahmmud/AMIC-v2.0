from django.contrib import admin
from .models import OTScheduleModel

class OTScheduleModelAdmin(admin.ModelAdmin):
	list_display = ('id', 'patient', 'date', 'start_time', 'end_time', 'status')
	list_filter = ('date', 'start_time', 'end_time', 'status')
	search_fields = ('patient', 'date', 'start_time', 'end_time', 'status')

admin.site.register(OTScheduleModel, OTScheduleModelAdmin)
