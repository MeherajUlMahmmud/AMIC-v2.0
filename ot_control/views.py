import datetime
from django.shortcuts import redirect, render
from ot_control.forms import OTScheduleForm

from ot_control.models import OTScheduleModel
from user_control.models import PatientModel, UserModel


def ot_booking_home_view(request):
    bookings = OTScheduleModel.objects.filter(
        date__range=[
            datetime.date.today(),
            datetime.date.today() + datetime.timedelta(days=7),
        ]
    ).order_by(
        "date"
    )  # get all bookings within the next 7 days

    context = {
        "bookings": bookings,
    }
    return render(request, "pages/ot/ot_booking_home.html", context)


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


def update_ot_booking_view(request, pk):
    task = "Update Operation Theater Booking"
    booking = OTScheduleModel.objects.get(id=pk)

    # check if the user is the owner of the booking
    if (
        request.user != booking.patient.user and booking.status != "Pending"
    ):  # if the user is not the owner of the booking
        return redirect("ot-booking-detail", pk)  # redirect to detail page

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


def delete_ot_booking_view(request, pk):
    booking = OTScheduleModel.objects.get(id=pk)

    # check if the user is the owner of the booking
    if (
        request.user != booking.patient.user and booking.status != "Pending"
    ):  # if the user is not the owner of the booking
        return redirect("ot-booking-detail", pk)  # redirect to detail page

    if request.method == "POST":
        booking.delete()
        return redirect("ot-booking-home")

    context = {
        "booking": booking,
    }
    return render(request, "pages/ot/ot_booking_delete.html", context)


def ot_booking_detail_view(request, pk):
    booking = OTScheduleModel.objects.get(id=pk)

    # check if the user is the owner of the booking
    my_booking = False
    if request.user == booking.patient.user:
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
    return render(request, "pages/ot/ot_booking_detail.html", context)


def users_ot_booking_view(request, pk):
    user = UserModel.objects.get(id=pk)
    patient = PatientModel.objects.get(user=user)  # get patient
    bookings = OTScheduleModel.objects.filter(patient=patient).order_by(
        "date"
    )  # get all bookings for the patient
    context = {
        "bookings": bookings,
    }
    return render(request, "pages/ot/users_ot_booking.html", context)
