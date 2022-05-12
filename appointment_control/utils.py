from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def filter_appointment_list(appointments):
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
    return (
        pending_appointments,
        upcoming_appointments,
        rejected_appointments,
        completed_appointments,
    )


def render_to_pdf(template_src, context):
    template = get_template(template_src)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None
