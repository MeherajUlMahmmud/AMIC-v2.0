from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from user_control.decorators import show_to_doctor, show_to_patient
from user_control.utils import calculate_age
from .forms import *
from .models import AppointmentModel
from user_control.models import (
    UserModel,
    DoctorModel,
    PatientModel,
    SpecializationModel,
)
from .utils import filter_appointment_list, render_to_pdf


@login_required(login_url="login")
@show_to_patient(allowed_roles=["is_patient"])
def patient_appointment_home_view(request):
    user = request.user
    patient = PatientModel.objects.get(user=user)
    appointments = AppointmentModel.objects.filter(patient=patient)
    filtered_appointments = filter_appointment_list(appointments)

    context = {
        "pending_appointments": filtered_appointments[0],
        "upcoming_appointments": filtered_appointments[1],
        "rejected_appointments": filtered_appointments[2],
        "completed_appointments": filtered_appointments[3],
    }
    return render(request, "pages/appointment/patient-appointment-home.html", context)


@login_required(login_url="login")
@show_to_doctor(allowed_roles=["is_doctor"])
def doctor_appointment_home_view(request):
    user = request.user
    doctor = DoctorModel.objects.get(user=user)
    appointments = AppointmentModel.objects.filter(doctor=doctor)

    pending_appointments = [
        appointment
        for appointment in appointments
        if appointment.is_accepted == False
        and appointment.is_canceled == False
        and appointment.is_complete == False
    ]
    upcoming_appointments = [
        appointment
        for appointment in appointments
        if appointment.is_accepted == True
        and appointment.is_canceled == False
        and appointment.is_complete == False
    ]
    rejected_appointments = [
        appointment
        for appointment in appointments
        if appointment.is_accepted == False
        and appointment.is_canceled == True
        and appointment.is_complete == False
    ]
    completed_appointments = [
        appointment
        for appointment in appointments
        if appointment.is_accepted == True
        and appointment.is_canceled == False
        and appointment.is_complete == True
    ]

    context = {
        "pending_appointments": pending_appointments,
        "upcoming_appointments": upcoming_appointments,
        "rejected_appointments": rejected_appointments,
        "completed_appointments": completed_appointments,
    }
    return render(request, "pages/appointment/doctor-appointment-home.html", context)


@login_required(login_url="login")
@show_to_patient(allowed_roles=["is_patient"])
def make_appointment_view(request, pk):
    doctor = DoctorModel.objects.get(user=UserModel.objects.get(id=pk))
    patient = PatientModel.objects.get(user=request.user)

    form = PatientAppointmentForm()
    if request.method == "POST":
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            new_appointment = form.save(commit=False)
            new_appointment.patient = patient
            new_appointment.doctor = doctor
            new_appointment.department = doctor.specialization
            new_appointment.save()
            return redirect("appointment-details", new_appointment.id)
        else:
            context = {
                "patient": patient,
                "doctor": doctor,
                "form": form,
            }
            return render(request, "pages/appointment/make-appointment.html", context)

    context = {
        "patient": patient,
        "doctor": doctor,
        "form": form,
    }
    return render(request, "pages/appointment/make-appointment.html", context)


@login_required(login_url="login")
@show_to_patient(allowed_roles=["is_patient"])
def patient_appointment_update_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)
    form = PatientAppointmentForm(instance=appointment)
    if request.method == "POST":
        form = PatientAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment.save()
            return redirect("appointment-details", appointment.id)

    context = {
        "appointment": appointment,
        "form": form,
    }
    return render(request, "pages/appointment/patient-update-appointment.html", context)


@login_required(login_url="login")
@show_to_doctor(allowed_roles=["is_doctor"])
def doctor_appointment_update_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)
    form = DoctorAppointmentForm(instance=appointment)
    if request.method == "POST":
        form = DoctorAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            appointment.is_accepted = True
            appointment.save()
            return redirect("appointment-details", appointment.id)

    context = {
        "appointment": appointment,
        "form": form,
    }
    return render(request, "pages/appointment/doctor-update-appointment.html", context)


@login_required(login_url="login")
@show_to_patient(allowed_roles=["is_patient"])
def appointment_delete_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)

    if request.method == "POST":
        appointment.delete()
        return redirect("patient-appointment-home")

    context = {
        "appointment": appointment,
    }
    return render(request, "pages/appointment/delete-appointment.html", context)


@login_required(login_url="login")
@show_to_doctor(allowed_roles=["is_doctor"])
def appointment_reject_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)

    if request.method == "POST":
        appointment.is_canceled = True
        appointment.save()
        return redirect("appointment-details", appointment.id)

    context = {
        "appointment": appointment,
    }
    return render(request, "pages/appointment/reject-appointment.html", context)


@login_required(login_url="login")
def appointment_detail_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)
    is_pending = False
    if (
        appointment.is_accepted == False
        and appointment.is_canceled == False
        and appointment.is_complete == False
    ):
        is_pending = True

    is_upcoming = False
    if (
        appointment.is_accepted == True
        and appointment.is_canceled == False
        and appointment.is_complete == False
    ):
        is_upcoming = True

    is_complete = False
    prescription = None
    if appointment.is_complete:
        is_complete = True
        prescription = PrescriptionModel.objects.get(appointment=appointment)

    context = {
        "appointment": appointment,
        "is_pending": is_pending,
        "is_complete": is_complete,
        "is_upcoming": is_upcoming,
        "prescription": prescription,
    }
    return render(request, "pages/appointment/appointment-details.html", context)


@login_required(login_url="login")
@show_to_doctor(allowed_roles=["is_doctor"])
def write_prescription_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)

    form = PrescriptionForm()
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()

            appointment.is_complete = True
            appointment.save()
            return redirect("appointment-details", appointment.id)
        else:
            context = {
                "appointment": appointment,
                "form": form,
            }
            return render(
                request, "pages/appointment/appointment-details.html", context
            )

    context = {
        "appointment": appointment,
        "form": form,
    }
    return render(request, "pages/appointment/write-prescription.html", context)


@login_required(login_url="login")
def pdf_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)

    patient = PatientModel.objects.get(user=appointment.patient.user)

    prescription = PrescriptionModel.objects.get(appointment=appointment)

    age = None
    if patient.date_of_birth:
        age = calculate_age(patient.date_of_birth)

    context = {
        "age": age,
        "appointment": appointment,
        "prescription": prescription,
    }
    pdf = render_to_pdf("pages/appointment/pdf.html", context)
    return HttpResponse(pdf, content_type="application/pdf")


@login_required(login_url="login")
@show_to_patient(allowed_roles=["is_patient"])
def appointment_doctor_list_view(request):
    specializations = SpecializationModel.objects.all()
    doctors = DoctorModel.objects.all()
    doctors = [doctor for doctor in doctors if doctor.specialization is not None]

    context = {
        "specializations": specializations,
        "doctors": doctors,
    }
    return render(request, "pages/appointment/doctors-list.html", context)
