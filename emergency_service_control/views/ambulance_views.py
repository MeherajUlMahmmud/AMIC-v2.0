from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from emergency_service_control.models import AmbulanceModel

def ambulance_home_view(request):
	ambulances = AmbulanceModel.objects.filter(available=True) # get all ambulances from the database

	paginator = Paginator(ambulances, 15) # Show 16 requests per page
	page = request.GET.get('page', 1) # get page number from url
	try:
		ambulances = paginator.page(page) # get the requested page
	except PageNotAnInteger: # if page is not an integer, deliver first page
		ambulances = paginator.page(1)
	except EmptyPage: # if page is out of range, deliver last page of results
		ambulances = paginator.page(paginator.num_pages)

	context = { 
        'ambulances': ambulances, # pass the ambulances to the context
    }
	return render(request, 'pages/emergency/ambulance/ambulance-home.html', context) # render the ambulance home page


def ambulance_detail_view(request, pk):
	ambulance = AmbulanceModel.objects.get(pk=pk) # get the ambulance from the database
	location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q=" + ambulance.city + "&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed" #

	context = {
		'ambulance': ambulance, # pass the ambulance to the context
		'location_link': location_link
	}
	return render(request, 'pages/emergency/ambulance/ambulance-detail.html', context) # render the ambulance detail page
