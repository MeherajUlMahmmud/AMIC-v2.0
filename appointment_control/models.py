from django.db import models

from user_control.models import PatientModel, DoctorModel


class AppointmentModel(models.Model):
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

    def __str__(self):
        return self.patient.user.name, "appointment with", self.doctor.user.name

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"


class PrescriptionModel(models.Model):
    appointment = models.ForeignKey(
        AppointmentModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    details = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.appointment.patient.user.name, "prescription"

    class Meta:
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"
