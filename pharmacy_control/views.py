from django.shortcuts import render


def pharmacy_home_view(request):
	return render(request, 'pages/pharmacy/pharmacy_home.html')
