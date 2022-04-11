from django.shortcuts import render


def ot_booking_home_view(request):
	return render(request, 'ot_control/ot_booking_home.html')


def ot_booking_post_view(request):
	return render(request, 'ot_control/ot_booking_post.html')


def update_ot_bookng_view(request):
	return render(request, 'ot_control/ot_booking_update.html')


def delete_ot_booking_view(request):
	return render(request, 'ot_control/ot_booking_delete.html')


def ot_booking_detail_view(request):
	return render(request, 'ot_control/ot_booking_detail.html')


def users_ot_booking_view(request):
	return render(request, 'ot_control/users_ot_booking.html')
