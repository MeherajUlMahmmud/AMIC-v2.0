from django.contrib import admin
from .models import *


class MedicineSectionModelAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_per_page = 25


class MedicineModelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "medicine_section",
        "price",
        "is_available",
        "available_quantity",
        "discount",
    ]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_per_page = 25


class MedicineCartModelAdmin(admin.ModelAdmin):
    list_display = ["user", "total_items", "total_price"]
    list_display_links = ["user"]
    search_fields = ["user"]
    list_per_page = 25


class MedicineCartItemModelAdmin(admin.ModelAdmin):
    list_display = ["medicine", "quantity", "price"]
    list_display_links = ["medicine"]
    search_fields = ["medicine"]
    list_per_page = 25


admin.site.register(MedicineSectionModel, MedicineSectionModelAdmin)
admin.site.register(MedicineModel, MedicineModelAdmin)
admin.site.register(MedicineCartModel, MedicineCartModelAdmin)
admin.site.register(MedicineCartItemModel, MedicineCartItemModelAdmin)
admin.site.register(MedicineOrderModel)
admin.site.register(MedicineOrderItemModel)
