import datetime
from django.shortcuts import redirect, render
from ot_control.forms import OTScheduleForm

from ot_control.models import OTScheduleModel
from user_control.models import PatientModel


def ot_booking_home_view(request):
	bookings = OTScheduleModel.objects.filter(date__gte=datetime.date.today()).order_by('date') # get all bookings within the next 7 days
	context = {
		'bookings': bookings,
	}
	return render(request, 'pages/ot/ot_booking_home.html', context)


def ot_booking_post_view(request):
	task = "Book Operation Theater"
	form = OTScheduleForm()
	if request.method == 'POST':
		form = OTScheduleForm(request.POST)
		if form.is_valid():
			booking = form.save(commit=False)
			user = request.user
			patient = PatientModel.objects.get(user=user)
			booking.patient = patient
			booking.save()
			return redirect('ot-booking-home')
	context = {
		'task': task,
		'form': form,
	}
	return render(request, 'pages/ot/ot_booking_create_update.html', context)


def update_ot_bookng_view(request):
	return render(request, 'pages/ot/ot_booking_create_update.html')


def delete_ot_booking_view(request):
	return render(request, 'pages/ot/ot_booking_delete.html')


def ot_booking_detail_view(request, pk):
	booking = OTScheduleModel.objects.get(pk=pk)
	context = {
		'booking': booking,
	}
	return render(request, 'pages/ot/ot_booking_detail.html', context)


def users_ot_booking_view(request):
	return render(request, 'pages/ot/users_ot_booking.html')
