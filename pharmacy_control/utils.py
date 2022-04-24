from .models import *


def cartItemToOrderItem(
    order, cart_items
):  # A function to convert cart items to order items
    for item in cart_items:  # For each item in the cart
        MedicineOrderItemModel.objects.create(
            medicine_order=order,
            medicine=item.medicine,
            quantity=item.quantity,
            price=item.price,
        )  # Create an order item
        item.delete()  # Delete the cart item
