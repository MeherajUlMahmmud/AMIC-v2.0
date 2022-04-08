from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from user_control.decorators import show_to_doctor, show_to_patient
from user_control.utils import calculate_age
from .forms import *
from .models import AppointmentModel
from user_control.models import UserModel, DoctorModel, PatientModel, SpecializationModel
from .utils import filter_appointment_list, render_to_pdf


@login_required(login_url='login')  # redirects to login if user is not logged in
@show_to_patient(allowed_roles=['is_patient'])  # accessible to patients only
def patient_appointment_home_view(request):
    """
    This is a view for the patient to see their current appointments

    :param request: the HttpRequest
    :return: a rendered page

    This view is only accessible to logged in users who are patients.
    Patients will be able to see their upcoming, pending, canceled and completed appointments on this page.
    """
    user = request.user  # get current user from request
    patient = PatientModel.objects.get(user=user)  # get current patient from user
    appointments = AppointmentModel.objects.filter(patient=patient)  # get all appointments for current patient
    filtered_appointments = filter_appointment_list(appointments)  # filter appointments based on state

    context = {  # create context to pass to frontend
        'pending_appointments': filtered_appointments[0],
        'upcoming_appointments': filtered_appointments[1],
        'rejected_appointments': filtered_appointments[2],
        'completed_appointments': filtered_appointments[3],
    }
    return render(request, 'pages/appointment/patient-appointment-home.html', context)  # render the page


@login_required(login_url='login')  # redirects to login if user is not logged in
@show_to_doctor(allowed_roles=['is_doctor'])  # accessible to doctors only
def doctor_appointment_home_view(request):
    """
    This is a view for the doctor to see their current appointments

    :param request: the HttpRequest
    :return: a rendered page

    This view is only accessible to logged in users who are doctors.
    Doctors will be able to see their upcoming, pending, canceled and completed appointments on this page.
    """
    user = request.user  # get current user from request
    doctor = DoctorModel.objects.get(user=user)  # get current doctor from user
    appointments = AppointmentModel.objects.filter(doctor=doctor)
    pending_appointments = [appointment for appointment in appointments
                            if appointment.is_accepted == False
                            and appointment.is_canceled == False
                            and appointment.is_complete == False]  # get all pending appointments
    upcoming_appointments = [appointment for appointment in appointments
                             if appointment.is_accepted == True
                             and appointment.is_canceled == False
                             and appointment.is_complete == False]  # get all upcoming appointments
    rejected_appointments = [appointment for appointment in appointments
                             if appointment.is_accepted == False
                             and appointment.is_canceled == True
                             and appointment.is_complete == False]  # get all rejected appointments
    completed_appointments = [appointment for appointment in appointments
                              if appointment.is_accepted == True
                              and appointment.is_canceled == False
                              and appointment.is_complete == True]  # get all completed appointments
    context = {  # create context to pass to frontend
        'pending_appointments': pending_appointments,
        'upcoming_appointments': upcoming_appointments,
        'rejected_appointments': rejected_appointments,
        'completed_appointments': completed_appointments,
    }
    return render(request, 'pages/appointment/doctor-appointment-home.html', context)  # render the page


@login_required(login_url='login')  # redirects to login if user is not logged in
@show_to_patient(allowed_roles=['is_patient'])  # accessible to patients only
def make_appointment_view(request, pk):
    """
    This is a view for the patient to make an appointment

    :param request: the HttpRequest
    :param pk: the primary key of the doctor to make an appointment with

    This view is only accessible to logged in users who are patients.
    Patients will be able to make an appointment with a doctor by entering their information and when they want to see the doctor.
    """
    doctor = DoctorModel.objects.get(user=UserModel.objects.get(id=pk))  # get current doctor from user
    patient = PatientModel.objects.get(user=request.user)  # get current patient from user

    form = PatientAppointmentForm()  # create empty form
    if request.method == 'POST':  # If the form has been submitted...
        form = PatientAppointmentForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            new_appointment = form.save(commit=False)  # Create a new AppointmentModel instance from the form
            new_appointment.patient = patient  # Set the patient for the new appointment
            new_appointment.doctor = doctor  # Set the doctor for the new appointment
            new_appointment.department = doctor.specialization  # Set the department for the new appointment
            new_appointment.save()  # Save the new appointment
            return redirect('appointment-details', new_appointment.id)  # Redirect after POST
        else:  # If the form is not valid
            context = {  # create context to pass to frontend
                'patient': patient,
                'doctor': doctor,
                'form': form,
            }
            return render(request, 'pages/appointment/make-appointment.html', context)

    context = {  # create context to pass to frontend
        'patient': patient,
        'doctor': doctor,
        'form': form,
    }
    return render(request, 'pages/appointment/make-appointment.html', context)


@login_required(login_url='login')  # redirects to login if user is not logged in
@show_to_patient(allowed_roles=['is_patient'])  # accessible to patients only
def patient_appointment_update_view(request, pk):
    """
    This is a view for the patient to update an appointment.

    :param request: the HttpRequest
    :param pk: the primary key of the appointment to update
    :return: a rendered page

    This view is only accessible to logged in users who are patients.
    Patients will be able to update an appointment from this page.
    """
    appointment = AppointmentModel.objects.get(id=pk)  # get current appointment from id
    form = PatientAppointmentForm(instance=appointment)  # create empty form
    if request.method == 'POST':  # If the form has been submitted...
        form = PatientAppointmentForm(request.POST, instance=appointment)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            appointment.save()  # Save the appointment
            return redirect('appointment-details', appointment.id)  # Redirect after POST

    context = {  # create context to pass to frontend
        'appointment': appointment,
        'form': form
    }
    return render(request, 'pages/appointment/patient-update-appointment.html', context)


@login_required(login_url='login')  # redirects to login if user is not logged in
@show_to_doctor(allowed_roles=['is_doctor'])  # accessible to doctors only
def doctor_appointment_update_view(request, pk):
    """
    This view is for a doctor to update an appointment.

    :param request: the HttpRequest
    :param pk: the primary key of the appointment to update
    :return: a rendered page

    This view is only accessible to logged in users who are doctors.
    Doctors will be able to update an appointment from this page.
    """
    appointment = AppointmentModel.objects.get(id=pk)  # get current appointment from id
    form = DoctorAppointmentForm(instance=appointment)  # create empty form
    if request.method == 'POST':  # If the form has been submitted...
        form = DoctorAppointmentForm(request.POST, instance=appointment)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            appointment = form.save()  # Save the form
            appointment.is_accepted = True  # Set the appointment to accepted
            appointment.save()  # Save the appointment
            return redirect('appointment-details', appointment.id)  # Redirect after POST

    context = {  # create context to pass to frontend
        'appointment': appointment,
        'form': form
    }
    return render(request, 'pages/appointment/doctor-update-appointment.html', context)


@login_required(login_url='login')  # redirects to login if user is not logged in
@show_to_patient(allowed_roles=['is_patient'])  # accessible to patients only
def appointment_delete_view(request, pk):  # delete appointment view
    """
    This view is for a patient to delete an appointment.

    :param request: the HttpRequest
    :param pk: the primary key of the appointment to delete
    :return: a rendered page

    This view is only accessible to logged in users who are patients.
    Patients will be able to delete an appointment from this page.
    """
    appointment = AppointmentModel.objects.get(id=pk)  # get current appointment from id

    if request.method == 'POST': # If the form has been submitted...
        appointment.delete() # Delete the appointment
        return redirect('patient-appointment-home') # Redirect to appointment home page

    context = {  # create context to pass to frontend
        'appointment': appointment,
    }
    return render(request, 'pages/appointment/delete-appointment.html', context)  # render the page


@login_required(login_url='login') # redirects to login if user is not logged in
@show_to_doctor(allowed_roles=['is_doctor']) # accessible to doctors only
def appointment_reject_view(request, pk):
    """
    This view is for a doctor to reject an appointment.

    :param request: the HttpRequest
    :param pk: the primary key of the appointment to reject
    :return: a rendered page

    This view is only accessible to logged in users who are doctors.
    Doctors will be able to reject an appointment from this page.
    """
    appointment = AppointmentModel.objects.get(id=pk)  # get current appointment from id

    if request.method == 'POST': # If the form has been submitted...
        appointment.is_canceled = True # Set the appointment to canceled
        appointment.save() # Save the appointment
        return redirect('appointment-details', appointment.id) # Redirect to appointment details page

    context = {  # create context to pass to frontend
        'appointment': appointment,
    }
    return render(request, 'pages/appointment/reject-appointment.html', context)  # render the page


@login_required(login_url='login')  # redirects to login if user is not logged in
def appointment_detail_view(request, pk):  # view details of an appointment
    """
    This is a view for a patient to view the details of an appointment.

    :param request: the HttpRequest
    :param pk: the primary key of the appointment to view
    :return: a rendered page

    This view is only accessible to logged in users.
    Users can view the detaiuls of his/her appointment from this page.
    This page will show the details of the appointment, including the patient, the doctor, the date and time, and the appointment status.
    """
    appointment = AppointmentModel.objects.get(id=pk) # get current appointment from id
    is_pending = False # set is_pending to false
    if appointment.is_accepted == False and appointment.is_canceled == False and appointment.is_complete == False: # if the appointment is not accepted, canceled, or complete
        is_pending = True # set is_pending to true

    is_upcoming = False # set is_upcoming to false
    if appointment.is_accepted == True and appointment.is_canceled == False and appointment.is_complete == False: # if the appointment is accepted but not complete
        is_upcoming = True # set is_upcoming to true

    is_complete = False # set is_complete to false
    prescription = None # set prescription to none
    if appointment.is_complete: # if the appointment is complete
        is_complete = True # set is_complete to true
        prescription = PrescriptionModel.objects.get(appointment=appointment) # get prescription from appointment

    context = { # create context to pass to frontend
        'appointment': appointment,
        'is_pending': is_pending,
        'is_complete': is_complete,
        'is_upcoming': is_upcoming,
        'prescription': prescription,
    }
    return render(request, 'pages/appointment/appointment-details.html', context) # render the page


@login_required(login_url='login')  # redirects to login if user is not logged in
@show_to_doctor(allowed_roles=['is_doctor'])  # accessible to doctors only
def write_prescription_view(request, pk):
    """
    This view is for a doctor to write a prescription.

    :param request: the HttpRequest
    :param pk: the primary key of the appointment to update
    :return: a rendered page

    This view is only accessible to logged in users who are doctors.
    Doctors will be able to write a prescription from this page.
    """
    appointment = AppointmentModel.objects.get(id=pk) # get current appointment from id

    form = PrescriptionForm() # create a new form
    if request.method == 'POST': # If the form has been submitted...
        form = PrescriptionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            prescription = form.save(commit=False) # create a new prescription
            prescription.appointment = appointment # add appointment to prescription
            prescription.save() # save prescription

            appointment.is_complete = True # set appointment to complete
            appointment.save() # save appointment
            return redirect('appointment-details', appointment.id) # redirect to appointment details page
        else: # the form is not valid
            context = { # create context to pass to frontend
                'appointment': appointment,
                'form': form,
            }
            return render(request, 'pages/appointment/appointment-details.html', context) # render the page

    context = {
        'appointment': appointment,
        'form': form,
    }
    return render(request, 'pages/appointment/write-prescription.html', context)


@login_required(login_url='login')  # redirects to login if user is not logged in
def pdf_view(request, pk):
    """
    This view is for a user (Patient or Doctor) to generate a PDF of a prescription.

    :param request: the HttpRequest
    :param pk: the primary key of the appointment
    :return: a rendered page

    This view is only accessible to logged in users.
    Doctors or Patients can generate a PDF of a prescription from this page.
    """
    appointment = AppointmentModel.objects.get(id=pk)  # get current appointment from id

    patient = PatientModel.objects.get(user=appointment.patient.user)  # get current patient from user

    prescription = PrescriptionModel.objects.get(appointment=appointment)  # get current prescription from appointment

    age = None
    if patient.date_of_birth:  # if patient has a date of birth
        age = calculate_age(patient.date_of_birth)  # calculate age

    context = { # create context to pass to frontend
        'age': age,
        'appointment': appointment,
        'prescription': prescription,
    }
    pdf = render_to_pdf('pages/appointment/pdf.html', context)  # create HttpResponse object with PDF content
    return HttpResponse(pdf, content_type='application/pdf')


@login_required(login_url='login')  # redirects to login if user is not logged in
@show_to_patient(allowed_roles=['is_patient'])  # accessible to patients only
def appointment_doctor_list_view(request):
    """
    This view returns a list of all the appointments for the current patient

    :param request: The HTTP request
    :return: The list of appointments

    Patients can see a list of all the doctors available to them and can select one to see the details of a specific doctor, and request an appointment with them.
    """
    specializations = SpecializationModel.objects.all() # get all specializations
    doctors = DoctorModel.objects.all() # get all doctors
    doctors = [doctor for doctor in doctors if doctor.specialization is not None] # get all doctors that have a specialization

    context = { # create context to pass to frontend
        'specializations': specializations,
        'doctors': doctors
    }
    return render(request, 'pages/appointment/doctors-list.html', context) # render the page
