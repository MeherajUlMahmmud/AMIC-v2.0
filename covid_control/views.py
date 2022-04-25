from django.shortcuts import render


def covid_home_view(request):
    return render(request, "pages/covid/covid_home.html")


def covid_post_view(request):
    return render(request, "pages/covid/covid_post_update.html")


def covid_update_view(request):
    return render(request, "pages/covid/covid_post_update.html")


def covid_delete_view(request):
    return render(request, "pages/covid/covid_delete.html")


def covid_detail_view(request):
    return render(request, "pages/covid/covid_detail.html")
