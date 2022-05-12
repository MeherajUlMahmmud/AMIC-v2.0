from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import TestBookingForm
from .models import TestModel


@login_required(login_url="login")
def pathology_home_view(request):
    bookings = TestModel.objects.filter(user=request.user).order_by("-created_at")

    pending_bookings = bookings.filter(status="Pending")
    completed_bookings = bookings.filter(status="Completed")
    in_progress_bookings = bookings.filter(status="In Progress")
    rejected_bookings = bookings.filter(status="Rejected")

    context = {
        "pending_bookings": pending_bookings,
        "completed_bookings": completed_bookings,
        "in_progress_bookings": in_progress_bookings,
        "rejected_bookings": rejected_bookings,
    }
    return render(request, "pages/pathology/pathology_home.html", context)


@login_required(login_url="login")
def pathology_post_view(request):
    task = "Book Pathology Test"
    form = TestBookingForm()
    if request.method == "POST":
        form = TestBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return render(request, "pages/pathology/pathology_home.html")
    context = {
        "task": task,
        "form": form,
    }
    return render(request, "pages/pathology/pathology_create_update.html", context)


@login_required(login_url="login")
def pathology_detail_view(request, pk):
    booking = TestModel.objects.get(id=pk)
    status = None
    if booking.status == "Pending":
        status = "Pending"
    elif booking.status == "Completed":
        status = "Completed"
    elif booking.status == "In Progress":
        status = "In Progress"
    elif booking.status == "Rejected":
        status = "Rejected"

    my_booking = False
    if request.user == booking.user:
        my_booking = True

    is_pending = False
    if booking.status == "Pending":
        is_pending = True

    context = {
        "booking": booking,
        "my_booking": my_booking,
        "is_pending": is_pending,
        "status": status,
    }
    return render(request, "pages/pathology/pathology_detail.html", context)


@login_required(login_url="login")
def update_pathology_view(request, pk):
    task = "Update Pathology Test Booking"
    booking = TestModel.objects.get(id=pk)

    if request.user != booking.user and booking.status != "Pending":
        return redirect("pathology-booking-detail", pk)

    form = TestBookingForm(instance=booking)
    if request.method == "POST":
        form = TestBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect("pathology-detail", pk)
    context = {
        "task": task,
        "form": form,
    }
    return render(request, "pages/pathology/pathology_create_update.html", context)


@login_required(login_url="login")
def delete_pathology_view(request, pk):
    booking = TestModel.objects.get(id=pk)

    if request.user != booking.user and booking.status != "Pending":
        return redirect("pathology-detail", pk)

    if request.method == "POST":
        booking.delete()
        return redirect("pathology-home")

    context = {"booking": booking}
    return render(request, "pages/pathology/pathology_delete.html", context)
