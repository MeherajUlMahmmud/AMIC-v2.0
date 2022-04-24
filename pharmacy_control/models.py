from django.db import models

from user_control.constants import (
    MEDICINE_TYPE_CHOICES,
    ORDER_STATUS_CHOICES,
    PAYMENT_METHOD_CHOICES,
    STATUS_CHOICES,
)
from user_control.models import UserModel


class MedicineSectionModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Medicine Section"
        verbose_name_plural = "Medicine Sections"


class MedicineModel(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=MEDICINE_TYPE_CHOICES)
    medicine_section = models.ForeignKey(MedicineSectionModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="medicine_images", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_details = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    available_quantity = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    generics = models.CharField(max_length=255, null=True, blank=True)
    indications = models.TextField(null=True, blank=True)
    dosage = models.TextField(null=True, blank=True)
    interaction = models.TextField(null=True, blank=True)
    contraindications = models.TextField(null=True, blank=True)
    side_effects = models.TextField(null=True, blank=True)
    pregnancy_lactation = models.TextField(null=True, blank=True)
    precautions = models.TextField(null=True, blank=True)
    theraputic_class = models.TextField(null=True, blank=True)
    storage = models.TextField(null=True, blank=True)
    pharmaceutical_name = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Medicine"
        verbose_name_plural = "Medicines"


class MedicineCartModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    total_items = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Medicine Cart"
        verbose_name_plural = "Medicine Carts"


class MedicineCartItemModel(models.Model):
    cart = models.ForeignKey(MedicineCartModel, on_delete=models.CASCADE)
    medicine = models.ForeignKey(MedicineModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.medicine.name

    class Meta:
        verbose_name = "Medicine Cart Item"
        verbose_name_plural = "Medicine Cart Items"


class MedicineOrderModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    total_items = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=100,
        default="Pending",
        choices=ORDER_STATUS_CHOICES,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.medicine.name

    class Meta:
        verbose_name = "Medicine Order"
        verbose_name_plural = "Medicine Orders"


class MedicineOrderItemModel(models.Model):
    medicine_order = models.ForeignKey(MedicineOrderModel, on_delete=models.CASCADE)
    medicine = models.ForeignKey(MedicineModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.medicine.name

    class Meta:
        verbose_name = "Medicine Order Item"
        verbose_name_plural = "Medicine Order Items"
