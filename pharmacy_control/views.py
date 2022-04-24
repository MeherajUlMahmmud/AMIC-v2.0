import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pharmacy_control.forms import OrderForm

from pharmacy_control.models import *
from pharmacy_control.utils import cartItemToOrderItem


def pharmacy_home_view(request):
    sections = MedicineSectionModel.objects.all()
    medicines = MedicineModel.objects.filter(is_available=True)

    total_cart_items = 0  # Total cart items
    if request.user.is_authenticated:  # If user is logged in
        cart = MedicineCartModel.objects.get(user=request.user)  # Get the cart
        # Get the cart items
        cart_items = MedicineCartItemModel.objects.filter(cart=cart)
        total_cart_items = cart_items.count()  # Total cart items

    if request.GET.get("AddToCart"):  # If the user clicked the add to cart button
        item_id = int(request.GET.get("medicineID"))  # Get the food id
        medicine_item = MedicineModel.objects.get(id=item_id)  # Get the food item
        if total_cart_items == 0:  # If the total cart items is 0
            MedicineCartItemModel.objects.create(
                cart=cart,
                medicine=medicine_item,
                quantity=1,
                price=medicine_item.price,
            )  # Create a cart item
            cart.total_items = cart.total_items + 1  # Increase the total cart items
            cart.total_price = (
                cart.total_price + medicine_item.price
            )  # Increase the total cart price
            cart.save()  # Save the cart
        else:  # If the total cart items is not 0
            for item in cart_items:  # For each cart item
                if (
                    item.medicine.name == medicine_item.name
                ):  # If the cart item name is the same as the food item name
                    item.quantity += 1  # Increase the quantity
                    item.price = (
                        item.quantity * item.medicine.price
                    )  # Set the item total
                    item.save()  # Save the cart item

                    cart.total_items = (
                        cart.total_items + 1
                    )  # Increase the total cart items
                    cart.total_price = (
                        cart.total_price + medicine_item.price
                    )  # Increase the total cart price
                    cart.save()  # Save the cart
                    return redirect("pharmacy-home")  # Redirect to the menu page

            MedicineCartItemModel.objects.create(
                cart=cart,
                medicine=medicine_item,
                quantity=1,
                price=medicine_item.price,
            )  # Create a cart item if the cart item name is not the same as the food item name
            cart.total_items = cart.total_items + 1  # Increase the total cart items
            cart.total_price = (
                cart.total_price + medicine_item.price
            )  # Increase the total cart price
            cart.save()  # Save the cart

        return redirect("pharmacy-home")  # Redirect to the menu page

    context = {
        "sections": sections,
        "medicines": medicines,
        "total_cart_items": total_cart_items,
    }
    return render(request, "pages/pharmacy/pharmacy_home.html", context)


def pharmacy_medicine_view(request, medicine_id):
    medicine = MedicineModel.objects.get(id=medicine_id)

    total_cart_items = 0  # Total cart items
    if request.user.is_authenticated:  # If user is logged in
        cart = MedicineCartModel.objects.get(user=request.user)  # Get the cart
        # Get the cart items
        cart_items = MedicineCartItemModel.objects.filter(cart=cart)
        total_cart_items = cart_items.count()  # Total cart items

    if request.GET.get("AddToCart"):  # If the user clicked the add to cart button
        item_id = int(request.GET.get("medicineID"))  # Get the food id
        medicine_item = MedicineModel.objects.get(id=item_id)  # Get the food item
        if total_cart_items == 0:  # If the total cart items is 0
            MedicineCartItemModel.objects.create(
                cart=cart,
                medicine=medicine_item,
                quantity=1,
                price=medicine_item.price,
            )  # Create a cart item
            cart.total_items = cart.total_items + 1  # Increase the total cart items
            cart.total_price = (
                cart.total_price + medicine_item.price
            )  # Increase the total cart price
            cart.save()  # Save the cart
        else:  # If the total cart items is not 0
            for item in cart_items:  # For each cart item
                if (
                    item.medicine.name == medicine_item.name
                ):  # If the cart item name is the same as the food item name
                    item.quantity += 1  # Increase the quantity
                    item.price = (
                        item.quantity * item.medicine.price
                    )  # Set the item total
                    item.save()  # Save the cart item

                    cart.total_items = (
                        cart.total_items + 1
                    )  # Increase the total cart items
                    cart.total_price = (
                        cart.total_price + medicine_item.price
                    )  # Increase the total cart price
                    cart.save()  # Save the cart
                    return redirect(
                        "medicine-details", medicine.id
                    )  # Redirect to the menu page

            MedicineCartItemModel.objects.create(
                cart=cart,
                medicine=medicine_item,
                quantity=1,
                price=medicine_item.price,
            )  # Create a cart item if the cart item name is not the same as the food item name
            cart.total_items = cart.total_items + 1  # Increase the total cart items
            cart.total_price = (
                cart.total_price + medicine_item.price
            )  # Increase the total cart price
            cart.save()  # Save the cart

    context = {"medicine": medicine, "total_cart_items": total_cart_items}
    return render(request, "pages/pharmacy/pharmacy_medicine_details.html", context)


@login_required(login_url="login")
def pharmacy_cart_view(request):
    cart = MedicineCartModel.objects.get(user=request.user)
    cart_items = MedicineCartItemModel.objects.filter(cart=cart)
    total_cart_items = cart_items.count()

    return render(
        request,
        "pages/pharmacy/pharmacy_cart.html",
        {"cart": cart, "cart_items": cart_items, "total_cart_items": total_cart_items},
    )


@csrf_exempt  # this is to allow the ajax request to be processed
def updateItem(request):  # Update Item Ajax Request
    data = json.loads(request.body)  # Get the data from the ajax request
    medicineID = data["medicineID"]  # Get the food id
    action = data["action"]  # Get the action
    print("Product: ", medicineID)  # Print the food id
    print("Action: ", action)  # Print the action

    user = request.user  # Get the logged in user
    medicine = MedicineModel.objects.get(id=medicineID)  # Get the food item
    cart = MedicineCartModel.objects.get(user=user)  # Get the cart
    cart_item = MedicineCartItemModel.objects.get(
        cart=cart, medicine=medicine
    )  # Get the cart item for the medicine item

    if action == "add":  # If the action is add
        cart_item.quantity = cart_item.quantity + 1  # Increase the quantity

        cart.total_items = cart.total_items + 1  # Increase the total cart items
        cart.total_price = (
            cart.total_price + medicine.price
        )  # Increase the total cart price
        cart.save()  # Save the cart item
    elif action == "remove":  # If the action is remove
        cart_item.quantity = cart_item.quantity - 1  # Decrease the quantity

        cart.total_items = cart.total_items - 1  # Decrease the total cart items
        cart.total_price = (
            cart.total_price - medicine.price
        )  # Decrease the total cart price
        cart.save()  # Save the cart item

    cart_item.price = (
        cart_item.quantity * medicine.price
    )  # Set the item total to the quantity times the food price
    cart_item.save()  # Save the cart item

    if cart_item.quantity <= 0:  # If the quantity is 0
        cart_item.delete()  # Delete the cart item

    return JsonResponse("Item added", safe=False)  # Return the response


@login_required(
    login_url="login"
)  # If user is not logged in redirect to the login page
def proceed_order(request):  # Proceed Order Page
    user = request.user  # Get the logged in user
    cart = MedicineCartModel.objects.get(
        user=user
    )  # Get the cart of the logged in user
    cart_items = MedicineCartItemModel.objects.filter(
        cart=cart
    )  # Get the cart items of the logged in user
    total_cart_items = cart_items.count()  # Total cart items
    total = cart.total_price  # Total price of the cart

    form = OrderForm()  # Create an order form
    # if request.method == "POST":  # If the request method is POST
    #     form = OrderForm(request.POST)  # Get the form data
    #     if form.is_valid():  # If the form is valid
    #         order = form.save(commit=False)  # Save the form data
    #         order.total_items = cart.total_items  # Set the total items
    #         order.total_price = cart.total_price  # Set the total price
    #         order.user = request.user  # Set the user
    #         order.save()  # Save the order
    #         cartItemToOrderItem(
    #             order, cart_items
    #         )  # Save the cart items to the order items
    #         return redirect(
    #             "confirm-order", order.id
    #         )  # Redirect to the confirm order page

    context = {  # Context for the proceed order page
        "total_cart_items": total_cart_items,  # Total cart items
        "total": total,  # Total amount
        "cart_items": cart_items,  # Cart items list
        "form": form,  # Order form
        "grand_total": total + 50,  # Grand total amount
    }
    return render(
        request, "pages/pharmacy/proceed-order.html", context
    )  # Render the page with the context


@login_required(
    login_url="login"
)  # If user is not logged in redirect to the login page
def confirm_order(request, pk):  # Confirm Order Page
    order = MedicineOrderModel.objects.get(id=pk)  # Get the order

    context = {  # Context for the confirm order page
        "total_cart_items": 0,  # Total cart items
        "order": order,  # Order object
    }
    return render(
        request, "pages/pharmacy/confirm-order.html", context
    )  # Render the page with the context


def order_details(request, pk):  # Order Details Page
    cart = MedicineCartModel.objects.get(
        user=request.user
    )  # Get the cart of the logged in user
    cart_items = MedicineCartItemModel.objects.filter(
        cart=cart
    )  # Get the cart items of the logged in user
    total_cart_items = cart_items.count()  # Total cart items

    order = MedicineOrderModel.objects.get(id=pk)  # Get the order
    order_items = MedicineOrderItemModel.objects.filter(
        order=order
    )  # Get the order items

    context = {  # Context for the order details page
        "total_cart_items": total_cart_items,  # Total cart items
        "order": order,  # Order object
        "order_items": order_items,  # Order items list
        "grand_total": order.total_price + 50,  # Grand total amount
    }
    return render(
        request, "pages/pharmacy/order-details.html", context
    )  # Render the page with the context
