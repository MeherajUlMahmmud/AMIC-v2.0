from django.shortcuts import redirect, render
from django.http import HttpResponse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_doctor:
            return redirect("doctor-dashboard")
        elif request.user.is_authenticated and request.user.is_patient:
            return redirect("patient-dashboard")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def show_to_doctor(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_doctor:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, "401.html")

        return wrapper_func

    return decorator


def show_to_patient(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_patient:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, "401.html")

        return wrapper_func

    return decorator
