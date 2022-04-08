from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def filter_appointment_list(appointments):
    """
    This is an utiliy function to filter a list of appointments.
    This function filters a list of appointments based on the appointment state.
    """
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
    return pending_appointments, upcoming_appointments, rejected_appointments, completed_appointments

def render_to_pdf(template_src, context={}):
    """
    This is an utiliy function to render a PDF from a Django template
    This function render a template into a pdf file.
    """
    template = get_template(template_src)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
