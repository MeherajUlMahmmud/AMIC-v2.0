import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from ot_control.forms import OTScheduleForm

from ot_control.models import OTScheduleModel
from user_control.models import PatientModel, UserModel


@login_required(login_url="login")
def ot_booking_home_view(request):
    today = datetime.date.today()
    seven_days_later = today + datetime.timedelta(days=6)
    bookings = OTScheduleModel.objects.filter(
        date__range=[today, seven_days_later]
    ).order_by("date")

    context = {
        "bookings": bookings,
        "today": today,
        "seven_days_later": seven_days_later,
    }
    return render(request, "pages/ot/ot_booking_home.html", context)


@login_required(login_url="login")
def ot_booking_post_view(request):
    task = "Book Operation Theater"
    form = OTScheduleForm()
    if request.method == "POST":
        form = OTScheduleForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            user = request.user
            patient = PatientModel.objects.get(user=user)
            booking.patient = patient
            booking.save()
            return redirect("ot-booking-detail", pk=booking.id)
    context = {
        "task": task,
        "form": form,
    }
    return render(request, "pages/ot/ot_booking_create_update.html", context)


@login_required(login_url="login")
def update_ot_booking_view(request, pk):
    task = "Update Operation Theater Booking"
    booking = OTScheduleModel.objects.get(id=pk)

    if request.user != booking.patient.user and booking.status != "Pending":
        return redirect("ot-booking-detail", pk)

    form = OTScheduleForm(instance=booking)
    if request.method == "POST":
        form = OTScheduleForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect("ot-booking-detail", pk)
    context = {
        "task": task,
        "form": form,
    }
    return render(request, "pages/ot/ot_booking_create_update.html", context)


@login_required(login_url="login")
def delete_ot_booking_view(request, pk):
    booking = OTScheduleModel.objects.get(id=pk)

    if request.user != booking.patient.user and booking.status != "Pending":
        return redirect("ot-booking-detail", pk)

    if request.method == "POST":
        booking.delete()
        return redirect("ot-booking-home")

    context = {
        "booking": booking,
    }
    return render(request, "pages/ot/ot_booking_delete.html", context)


@login_required(login_url="login")
def ot_booking_detail_view(request, pk):
    booking = OTScheduleModel.objects.get(id=pk)

    my_booking = False
    if request.user == booking.patient.user:
        my_booking = True

    is_pending = False
    if booking.status == "Pending":
        is_pending = True
    context = {
        "booking": booking,
        "my_booking": my_booking,
        "is_pending": is_pending,
    }
    return render(request, "pages/ot/ot_booking_detail.html", context)


@login_required(login_url="login")
def users_ot_booking_view(request, pk):
    user = UserModel.objects.get(id=pk)
    patient = PatientModel.objects.get(user=user)
    bookings = OTScheduleModel.objects.filter(patient=patient).order_by("date")
    context = {
        "bookings": bookings,
    }
    return render(request, "pages/ot/users_ot_booking.html", context)
