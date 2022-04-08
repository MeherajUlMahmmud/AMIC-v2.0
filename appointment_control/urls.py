from django.urls import path

import appointment_control.views as views

urlpatterns = [
    path('', views.patient_appointment_home_view, name='patient-appointment-home'),
    path('home', views.doctor_appointment_home_view, name='doctor-appointment-home'),
    path('appointment/<str:pk>', views.appointment_detail_view, name='appointment-details'),
    path('make-appointment/<int:pk>', views.make_appointment_view, name='make-appointment'),
    path('appointment/<int:pk>/update', views.doctor_appointment_update_view, name='doctor-appointment-update'),
    path('update/<int:pk>', views.patient_appointment_update_view, name='patient-appointment-update'),
    path('appointment/<int:pk>/delete', views.appointment_delete_view, name='appointment-delete'),
    path('appointment/<int:pk>/reject', views.appointment_reject_view, name='appointment-reject'),
    path('doctors', views.appointment_doctor_list_view, name='appointment-doctors-list'),

    path('write-prescription/<int:pk>', views.write_prescription_view, name='write-prescription'),
    path('download-prescription/<str:pk>', views.pdf_view, name='pdf-view'),   
]
