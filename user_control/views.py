from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from appointment_control.models import AppointmentModel
from article_control.models import ArticleModel
from patient_community_control.models import CommunityPostModel
from pharmacy_control.models import MedicineCartModel
from emergency_service_control.models import BloodRequestModel, PlasmaRequestModel
from user_control.decorators import *
from user_control.forms import *
from user_control.utils import calculate_age


@unauthenticated_user
def home_view(request):
    return render(request, "index.html")


@unauthenticated_user
def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user and user.is_doctor:
                login(request, user)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect("doctor-dashboard")

            elif user and user.is_patient:
                login(request, user)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect("patient-dashboard")
            else:
                messages.error(request, "Email or Password is incorrect.")
                return redirect("login")
        else:
            return render(request, "authentication/login.html", {"form": form})

    form = LoginForm()
    context = {"form": form}
    return render(request, "authentication/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


@unauthenticated_user
def doctor_signup_view(request):
    if request.method == "POST":
        doctor_form = DoctorRegistrationForm(request.POST)
        if doctor_form.is_valid():
            doctor_form.save()
            email = request.POST["email"]
            password = request.POST["password1"]
            user = authenticate(request, email=email, password=password)
            user.is_doctor = True
            user.save()
            DoctorModel.objects.create(user=user)
            MedicineCartModel.objects.create(user=user)
            login(request, user)
            return redirect("doctor-dashboard")
        else:
            context = {"doctor_form": doctor_form}
            return render(request, "authentication/doctor-signup.html", context)
    else:
        doctor_form = DoctorRegistrationForm()

    context = {"doctor_form": doctor_form}
    return render(request, "authentication/doctor-signup.html", context)


@unauthenticated_user
def patient_signup_view(request):
    if request.method == "POST":
        patient_form = PatientRegistrationForm(request.POST)
        if patient_form.is_valid():
            patient_form.save()
            email = request.POST["email"]
            password = request.POST["password1"]
            user = authenticate(request, email=email, password=password)
            user.is_patient = True
            user.save()
            PatientModel.objects.create(user=user)
            MedicineCartModel.objects.create(user=user)
            login(request, user)
            return redirect("patient-dashboard")
        else:
            context = {"patient_form": patient_form}
            return render(request, "authentication/patient-signup.html", context)
    else:
        patient_form = PatientRegistrationForm()

    context = {"patient_form": patient_form}
    return render(request, "authentication/patient-signup.html", context)


@login_required(login_url="login")
@show_to_doctor(allowed_roles=["is_doctor"])
def doctor_dashboard(request):
    user = request.user
    profile = DoctorModel.objects.get(user=user)

    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, "pages/user-control/doctor-dashboard.html", context)


@login_required(login_url="login")
@show_to_patient(allowed_roles=["is_patient"])
def patient_dashboard(request):
    user = request.user
    profile = PatientModel.objects.get(user=user)

    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, "pages/user-control/patient-dashboard.html", context)


@login_required(login_url="login")
def doctor_profile_view(request, pk):
    is_self = False
    user = UserModel.objects.get(id=pk)

    if request.user == user:
        is_self = True

    profile = DoctorModel.objects.get(user=user)

    date_joined = calculate_age(user.date_joined)

    incomplete_profile = False
    if (
        not profile.bio
        or not profile.gender
        or not profile.blood_group
        or not profile.date_of_birth
        or not profile.phone
        or not profile.NID
        or not profile.specialization
        or not profile.BMDC_regNo
    ):
        incomplete_profile = True

    articles = ArticleModel.objects.filter(author=user)[:4]
    completed_appointments = AppointmentModel.objects.filter(
        doctor=profile, is_complete=True
    )

    is_pending = False
    if request.user.is_patient:
        patient = PatientModel.objects.get(user=request.user)
        appointments = AppointmentModel.objects.filter(
            patient=patient,
            doctor=profile,
            is_accepted=False,
            is_canceled=False,
            is_complete=False,
        )
        if appointments.count() > 0:
            is_pending = True

    context = {
        "user": user,
        "is_self": is_self,
        "profile": profile,
        "date_joined": date_joined,
        "completed_appointments": completed_appointments.count(),
        "incomplete_profile": incomplete_profile,
        "articles": articles,
        "total_posts": articles.count(),
        "is_pending": is_pending,
    }
    return render(request, "pages/user-control/doctor-profile.html", context)


@login_required(login_url="login")
def patient_profile_view(request, pk):
    is_self = False

    user = UserModel.objects.get(id=pk)
    if request.user == user:
        is_self = True

    has_access = True

    profile = PatientModel.objects.get(user=user)

    date_joined = calculate_age(user.date_joined)

    age = None
    if profile.date_of_birth:
        age = calculate_age(profile.date_of_birth)

    community_posts = CommunityPostModel.objects.filter(author=user)[:4]
    completed_appointments = AppointmentModel.objects.filter(
        patient=profile, is_complete=True
    )

    user = UserModel.objects.get(id=pk)
    blood_requests = BloodRequestModel.objects.filter(user=user).order_by("-created_at")
    plasma_requests = PlasmaRequestModel.objects.filter(user=user).order_by(
        "-created_at"
    )

    incomplete_profile = False
    if (
        not profile.gender
        or not profile.blood_group
        or not profile.date_of_birth
        or not profile.phone
        or not profile.height
        or not profile.weight
        or not profile.address
    ):
        incomplete_profile = True

    context = {
        "user": user,
        "is_self": is_self,
        "has_access": has_access,
        "age": age,
        "profile": profile,
        "date_joined": date_joined,
        "incomplete_profile": incomplete_profile,
        "community_posts": community_posts,
        "completed_appointments": completed_appointments.count(),
        "total_posts": community_posts.count(),
        "blood_requests": blood_requests[:4],
        "total_blood_requests": blood_requests.count(),
        "plasma_requests": plasma_requests[:4],
        "total_plasma_requests": plasma_requests.count(),
    }
    return render(request, "pages/user-control/patient-profile.html", context)


@login_required(login_url="login")
def doctor_edit_profile(request):
    user = request.user
    profile = DoctorModel.objects.get(user=user)

    form = DoctorEditProfileForm(instance=profile)
    if request.method == "POST":
        form = DoctorEditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("doctor-profile", user.id)
        else:
            return redirect("edit-profile")

    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "pages/user-control/edit-profile.html", context)


@login_required(login_url="login")
def patient_edit_profile(request):
    user = request.user
    profile = PatientModel.objects.get(user=user)

    form = PatientEditProfileForm(instance=profile)
    if request.method == "POST":
        form = PatientEditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("patient-profile", user.id)
        else:
            return redirect("patient-edit-profile")

    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "pages/user-control/edit-profile.html", context)


def contact_view(request):
    if request.method == "POST":
        name = request.POST["name"]
        email_add = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]

        FeedbackModel.objects.create(
            name=name, email=email_add, subject=subject, message=message
        )

        messages.success(request, "Feedback sent successfully.")

        return render(request, "pages/utils/contact.html")

    return render(request, "pages/utils/contact.html")


@login_required(login_url="login")
def account_settings_view(request):
    user = request.user

    information_form = AccountInformationForm(instance=user)
    password_form = PasswordChangeForm(request.user)
    if request.method == "POST":
        information_form = AccountInformationForm(request.POST, instance=user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if information_form.is_valid():
            information_form.save()
            user.save()
            return redirect("account-settings")

        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("account-settings")
        else:
            context = {
                "information_form": information_form,
                "password_form": password_form,
            }
            return render(request, "pages/user-control/account-settings.html", context)
    context = {
        "information_form": information_form,
        "password_form": password_form,
    }
    return render(request, "pages/user-control/account-settings.html", context)
