from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import CovidTestBookingForm
from .models import CovidTestModel


@login_required(login_url="login")
def covid_home_view(request):
    bookings = CovidTestModel.objects.filter(user=request.user).order_by("-created_at")

    pending_bookings = bookings.filter(status="Pending")
    upcoming_bookings = bookings.filter(status="Approved")
    completed_bookings = bookings.filter(status="Completed")
    in_progress_bookings = bookings.filter(status="In Progress")
    rejected_bookings = bookings.filter(status="Rejected")

    context = {
        "pending_bookings": pending_bookings,
        "upcoming_bookings": upcoming_bookings,
        "completed_bookings": completed_bookings,
        "in_progress_bookings": in_progress_bookings,
        "rejected_bookings": rejected_bookings,
        "pending_bookings_count": pending_bookings.count(),
        "upcoming_bookings_count": upcoming_bookings.count(),
        "completed_bookings_count": completed_bookings.count(),
        "in_progress_bookings_count": in_progress_bookings.count(),
        "rejected_bookings_count": rejected_bookings.count(),
    }
    return render(request, "pages/covid/covid_home.html", context)


@login_required(login_url="login")
def covid_detail_view(request, pk):
    booking = CovidTestModel.objects.get(id=pk)

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
    return render(request, "pages/covid/covid_detail.html", context)


@login_required(login_url="login")
def covid_post_view(request):
    task = "Book Covid Test"
    form = CovidTestBookingForm()
    if request.method == "POST":
        form = CovidTestBookingForm(request.POST)
        print(form.errors)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect("covid-home")
    context = {
        "task": task,
        "form": form,
    }
    return render(request, "pages/covid/covid_post_update.html", context)


@login_required(login_url="login")
def covid_update_view(request, pk):
    task = "Update Covid Test Booking"
    booking = CovidTestModel.objects.get(id=pk)

    if request.user != booking.user and booking.status != "Pending":
        return redirect("covid-detail", pk)

    form = CovidTestBookingForm(instance=booking)
    if request.method == "POST":
        form = CovidTestBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect("covid-detail", pk)

    context = {
        "task": task,
        "form": form,
    }
    return render(request, "pages/covid/covid_post_update.html", context)


@login_required(login_url="login")
def covid_delete_view(request, pk):
    booking = CovidTestModel.objects.get(id=pk)

    if request.user != booking.user and booking.status != "Pending":
        return redirect("covid-detail", pk)

    if request.method == "POST":
        booking.delete()
        return redirect("covid-home")

    context = {"booking": booking}
    return render(request, "pages/covid/covid_delete.html", context)
