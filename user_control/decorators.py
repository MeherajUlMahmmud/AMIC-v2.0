from django.shortcuts import redirect, render
from django.http import HttpResponse


def unauthenticated_user(view_func):
    """
    This is a decorator for views that checks that the user is logged in,
    redirecting to the login page if necessary.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_doctor:
            return redirect('doctor-dashboard')
        elif request.user.is_authenticated and request.user.is_patient:
            return redirect('patient-dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def show_to_doctor(allowed_roles=[]): 
    """
    This is a decorator for views that checks that the user is a doctor,
    show a HttpResponse if not.
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_doctor:
                return view_func(request, *args, **kwargs)
            else:
                # return HttpResponse("You are not authorized to view this page")
                return render(request, '401.html')

        return wrapper_func

    return decorator


def show_to_patient(allowed_roles=[]):
    """
    This is a decorator for views that checks that the user is a patient,
    show a HttpResponse if not.
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_patient:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, '401.html')

        return wrapper_func

    return decorator
