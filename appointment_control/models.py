from django.db import models

from user_control.models import PatientModel, DoctorModel


class AppointmentModel(models.Model):
    """
    This is the model for the appointment.
    The fields are:
    - patient: The patient that is making the appointment.
    - doctor: The doctor's appointment the patient wants.
    - date: The date of the appointment.
    - time: The time of the appointment.
    - is_accepted: The status of the appointment (accepted or not).
    - is_canceled: The status of the appointment (canceled or not).
    - is_complete: The status of the appointment (completed or not).
    - meet_link: The google meet link for the appointment.
    - notes: The notes the patient wants to add to the appointment.
    - created_at: The date and time the appointment was created.
    """
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    meet_link = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PrescriptionModel(models.Model):
    """
    This is the model for the prescription.
    The fields are:
    - appointment: The appointment the prescription belongs to.
    - details: The details of the prescription.
    -created_on: The date and time the prescription was created.
    """
    appointment = models.ForeignKey(
        AppointmentModel, on_delete=models.SET_NULL, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
