from django.shortcuts import redirect, render
from pathology_control.forms import TestBookingForm

from pathology_control.models import TestModel


def pathology_home_view(request):
    bookings = TestModel.objects.filter(user=request.user).order_by("--created_at")

    pending_bookings = bookings.filter(status="pending")
    completed_bookings = bookings.filter(status="completed")
    in_progress_bookings = bookings.filter(status="in progress")
    rejected_bookings = bookings.filter(status="rejected")
    context = {
        "pending_bookings": pending_bookings,
        "completed_bookings": completed_bookings,
        "in_progress_bookings": in_progress_bookings,
        "rejected_bookings": rejected_bookings,
    }
    return render(request, "pages/pathology/pathology_home.html", context)


def pathology_post_view(request):
    task = "Book Pathology Test"
    form = TestBookingForm()
    if request.method == "POST":
        form = TestBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "pages/pathology/pathology_home.html")
    context = {
        "task": task,
        "form": form,
    }
    return render(request, "pages/pathology/pathology_post.html", context)


def pathology_detail_view(request, pk):
    booking = TestModel.objects.get(id=pk)

    # check if the user is the owner of the booking
    my_booking = False
    if request.user == booking.user:
        my_booking = True

    # check if the booking is in the future
    is_pending = False
    if booking.status == "Pending":
        is_pending = True

    context = {
        "booking": booking,
        "my_booking": my_booking,
        "is_pending": is_pending,
    }
    return render(request, "pages/pathology/pathology_detail.html", context)


def update_pathology_view(request, pk):
    task = "Update Pathology Test Booking"
    booking = TestModel.objects.get(id=pk)

    # check if the user is the owner of the booking
    if (
        request.user != booking.user and booking.status != "Pending"
    ):  # if the user is not the owner of the booking
        return redirect("pathology-booking-detail", pk)  # redirect to detail page

    form = TestBookingForm(instance=booking)
    if request.method == "POST":
        form = TestBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect("pathology-booking-detail", pk)
    context = {
        "task": task,
        "form": form,
    }
    return render(request, "pages/pathology/update_pathology.html", context)


def delete_pathology_view(request, pk):
    booking = TestModel.objects.get(id=pk)

    # check if the user is the owner of the booking
    if (
        request.user != booking.user and booking.status != "Pending"
    ):  # if the user is not the owner of the booking
        return redirect("pathology-booking-detail", pk)  # redirect to detail page

    if request.method == "POST":
        booking.delete()
        return redirect("pathology-booking-home")

    context = {"booking": booking}
    return render(request, "pages/pathology/delete_pathology.html", context)
