from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from appointment_control.models import AppointmentModel
from article_control.models import ArticleModel
from patient_community_control.models import CommunityPostModel
from emergency_service_control.models import BloodRequestModel, PlasmaRequestModel
from user_control.decorators import *
from user_control.forms import *
from user_control.utils import calculate_age


@unauthenticated_user  # this decorator will ensure that the user is logged in before they can access this view
def home_view(request):  # The home page
    """
    This view will render the home page.
    :param request:
    :return: renders the home page
    """
    return render(request, 'index.html')


@unauthenticated_user  # this decorator will ensure that the user is logged in before they can access this view
def login_view(request):  # Log a user in
    """
    This view will render the login page.
    :param request:

    This view renders a login form and then takes in an email and a password.
    if the email and password is authentic then logs in the user otherwise shows an error.

    :return: renders the login page
    """
    if request.POST:  # If the form has been submitted...
        form = LoginForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            email = request.POST['email']  # Get the email
            password = request.POST['password']  # Get the password
            user = authenticate(email=email, password=password)  # Authenticate the user

            if user and user.is_doctor:  # If the user exists and is a doctor
                login(request, user)  # Log them in
                if request.GET.get('next'):  # If there is a next page
                    return redirect(request.GET.get('next'))  # Redirect to the next page
                return redirect('doctor-dashboard')  # Redirect to the doctor dashboard

            elif user and user.is_patient:  # If the user exists and is a patient
                login(request, user)  # Log them in
                if request.GET.get('next'):  # If there is a next page
                    return redirect(request.GET.get('next'))  # Redirect to the next page
                return redirect('patient-dashboard')  # Redirect to the patient dashboard
            else:  # If the user doesn't exist
                messages.error(request, 'Email or Password is incorrect.')  # Display an error message
                return redirect('login')  # Redirect to the login page
        else:  # The form is invalid
            return render(request, 'authentication/login.html', {'form': form})  # Render the login page

    form = LoginForm()  # An unbound form
    context = {  # Context to render the form
        'form': form  # The form
    }
    return render(request, 'authentication/login.html', context)  # Render the login page


def logout_view(request):  # Log a user out
    """
    This view will log a user out.
    :param request:

    This view logs out an user and redirects to the home page.

    :return: redirects to the home page
    """
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to the home page


@unauthenticated_user # this decorator will ensure that the user is logged in before they can access this view
def doctor_signup_view(request):  # The doctor signup page
    """
    This view will render the doctor signup page.
    :param request: The HTTP request

    This view renders a doctor signup form and then takes in an email and a password.
    if the email and password is authentic then logs in the user otherwise shows an error.

    :return: renders the doctor signup page
    """
    if request.method == "POST":  # If the form has been submitted...
        doctor_form = DoctorRegistrationForm(request.POST)  # A form bound to the POST data
        if doctor_form.is_valid():  # All validation rules pass
            doctor_form.save()  # Save the form
            email = request.POST['email']  # Get the email
            password = request.POST['password1']  # Get the password
            user = authenticate(request, email=email, password=password)  # Authenticate the user
            user.is_doctor = True
            user.save()  # Save the user
            DoctorModel.objects.create(user=user)  # Create a doctor record for the user
            login(request, user)  # Log the user in
            return redirect('doctor-dashboard')  # Redirect to the doctor dashboard
        else:  # The form is invalid
            context = {  # Context to render the form
                'doctor_form': doctor_form  # The form
            }
            return render(request, 'authentication/doctor-signup.html', context)  # Render the signup page
    else:  # The form has not been submitted
        doctor_form = DoctorRegistrationForm()  # An unbound form

    context = {  # Context to render the form
        'doctor_form': doctor_form  # The form
    }
    return render(request, 'authentication/doctor-signup.html', context)  # Render the signup page


@unauthenticated_user
def patient_signup_view(request):  # The patient signup page
    """
    This view will render the patient signup page.
    :param request:

    This view renders a patient signup form and then takes in an email and a password.
    if the email and password is authentic then logs in the user otherwise shows an error.

    :return: renders the patient signup page
    """
    if request.method == "POST":  # If the form has been submitted...
        patient_form = PatientRegistrationForm(request.POST)  # A form bound to the POST data
        if patient_form.is_valid():  # All validation rules pass
            patient_form.save()  # Save the form
            email = request.POST['email']  # Get the email
            password = request.POST['password1']  # Get the password
            user = authenticate(request, email=email, password=password)  # Authenticate the user
            user.is_patient = True
            user.save()  # Save the user
            PatientModel.objects.create(user=user)  # Create a patient model for the user
            login(request, user)  # Log the user in
            return redirect('patient-dashboard')  # Redirect to the patient dashboard
        else:  # The form is invalid
            context = {  # Context to render the form
                'patient_form': patient_form  # The form
            }
            return render(request, 'authentication/patient-signup.html', context)  # Render the signup page
    else:  # The form has not been submitted
        patient_form = PatientRegistrationForm()  # An unbound form

    context = {  # Context to render the form
        'patient_form': patient_form  # The form
    }
    return render(request, 'authentication/patient-signup.html', context)  # Render the signup page


@login_required(
    login_url='login')  # This decorator will ensure that the user is logged in before they can access this view
@show_to_doctor(allowed_roles=[
    'is_doctor'])  # This decorator will ensure that the user is a doctor before they can access this view
def doctor_dashboard(request):  # The doctor dashboard
    """
    This view will render the doctor dashboard.
    :param request:
    :return: renders the doctor dashboard
    """
    user = request.user  # Get the user
    profile = DoctorModel.objects.get(user=user)  # Get the doctor's profile

    context = {  # Context to render the view
        'user': user,  # The user
        'profile': profile,  # The doctor's profile
    }
    return render(request, 'pages/user-control/doctor-dashboard.html', context)  # Render the view


@login_required(login_url='login')
@show_to_patient(allowed_roles=[
    'is_patient'])  # This decorator will ensure that the user is a patient before they can access this view
def patient_dashboard(request):  # The patient dashboard
    """
    This view will render the patient dashboard.
    :param request:
    :return: renders the patient dashboard    
    """
    user = request.user  # Get the user
    profile = PatientModel.objects.get(user=user)  # Get the patient's profile

    context = {  # Context to render the view
        'user': user,  # The user
        'profile': profile,  # The patient's profile
    }
    return render(request, 'pages/user-control/patient-dashboard.html', context)  # Render the view


@login_required(login_url='login')
def doctor_profile_view(request, pk):  # The doctor's profile page
    """
    This view will render the doctor's profile page.
    :param request:
    :param pk: the primary key of the doctor

    This view will render the doctor's profile page, along with the informations like the name, email, phone number, posted articles, appointements, etc.

    :return: renders the doctor's profile page
    """
    is_self = False  # The user is not the doctor
    user = UserModel.objects.get(id=pk)  # Get the user

    if request.user == user:  # If the user is the doctor
        is_self = True  # Set the flag to True

    profile = DoctorModel.objects.get(user=user)  # Get the doctor's profile

    date_joined = calculate_age(user.date_joined)  # Get the age of the user account

    incomplete_profile = False
    if not profile.bio or not profile.gender or not profile.blood_group or not profile.date_of_birth or not \
            profile.phone or not profile.NID or not profile.specialization or not profile.BMDC_regNo:
        incomplete_profile = True

    articles = ArticleModel.objects.filter(author=user)[:4]
    completed_appointments = AppointmentModel.objects.filter(doctor=profile, is_complete=True)

    is_pending = False
    if request.user.is_patient:
        patient = PatientModel.objects.get(user=request.user)
        appointments = AppointmentModel.objects.filter(patient=patient, doctor=profile, is_accepted=False,
                                                       is_canceled=False, is_complete=False)
        if appointments.count() > 0:
            is_pending = True

    context = {  # Context to render the view
        'user': user,  # The user
        'is_self': is_self,  # The flag
        'profile': profile,  # The doctor's profile
        'date_joined': date_joined,  # The account age
        'completed_appointments': completed_appointments.count(),
        'incomplete_profile': incomplete_profile,
        'articles': articles,
        'total_posts': articles.count(),
        'is_pending': is_pending,
    }
    return render(request, "pages/user-control/doctor-profile.html", context)  # Render the view


@login_required(login_url='login')
def patient_profile_view(request, pk):  # The patient's profile page
    """
    This view will render the patient's profile page.
    :param request:
    :param pk: the primary key of the patient

    This view will render the patient's profile page, along with the informations like the name, email, phone number, community posts, completed appointements, blood requests, plasma requests, etc.

    :return: renders the patient's profile page    
    """
    is_self = False  # The user is not the patient

    user = UserModel.objects.get(id=pk)  # Get the user
    if request.user == user:  # If the user is the patient
        is_self = True  # Set the flag to True

    has_access = True

    profile = PatientModel.objects.get(user=user)  # Get the patient's profile

    date_joined = calculate_age(user.date_joined)  # Get the age of the user account

    age = None  # The age of the user
    if profile.date_of_birth:  # If the patient has a date of birth
        age = calculate_age(profile.date_of_birth)  # Get the age of the patient

    community_posts = CommunityPostModel.objects.filter(author=user)[:4]
    completed_appointments = AppointmentModel.objects.filter(patient=profile, is_complete=True)

    user = UserModel.objects.get(id=pk)
    # blood_requests = BloodRequestModel.objects.filter(user=user).order_by('-posted_on')
    # plasma_requests = PlasmaRequestModel.objects.filter(user=user).order_by('-posted_on')

    incomplete_profile = False
    if not profile.gender or not profile.blood_group or not profile.date_of_birth or not \
            profile.phone or not profile.height or not profile.weight or not profile.address:
        incomplete_profile = True

    context = {  # Context to render the view
        'user': user,  # The user
        'is_self': is_self,  # The flag
        'has_access': has_access,
        'age': age,  # The age
        'profile': profile,  # The patient's profile
        'date_joined': date_joined,  # The account age
        'incomplete_profile': incomplete_profile,
        'community_posts': community_posts,
        'completed_appointments': completed_appointments.count(),
        'total_posts': community_posts.count(),
        # 'blood_requests': blood_requests[:4],
        # 'total_blood_requests': blood_requests.count(),
        # 'plasma_requests': plasma_requests[:4],
        # 'total_plasma_requests': plasma_requests.count(),
    }
    return render(request, "pages/user-control/patient-profile.html", context)  # Render the view


@login_required(login_url='login')
def doctor_edit_profile(request):  # The doctor's profile edit page
    """
    This view will render the doctor's profile edit page.
    :param request:

    This view will render a form to edit the doctor's profile.

    :return: renders the doctor's profile edit page
    """
    user = request.user
    profile = DoctorModel.objects.get(user=user)  # Get the doctor's profile

    form = DoctorEditProfileForm(instance=profile)  # A form bound to the doctor's profile
    if request.method == 'POST':  # If the form has been submitted...
        form = DoctorEditProfileForm(request.POST, request.FILES, instance=profile)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            form.save()  # Save the form
            return redirect('doctor-profile', user.id)  # Redirect to the doctor's profile
        else:  # The form is invalid
            return redirect('edit-profile')  # Redirect to the edit profile page

    context = {  # Context to render the view
        'form': form,  # The form
        'profile': profile,  # The doctor's profile
    }
    return render(request, 'pages/user-control/edit-profile.html', context)  # Render the view


@login_required(login_url='login')
def patient_edit_profile(request):  # The patient's profile edit page
    """
    This view will render the patient's profile edit page.
    :param request:

    This view will render a form to edit the patient's profile.

    :return: renders the patient's profile edit page
    """
    user = request.user
    profile = PatientModel.objects.get(user=user)  # Get the patient's profile

    form = PatientEditProfileForm(instance=profile)  # A form bound to the patient's profile
    if request.method == 'POST':  # If the form has been submitted...
        form = PatientEditProfileForm(request.POST, request.FILES, instance=profile)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            form.save()  # Save the form
            return redirect('patient-profile', user.id)  # Redirect to the patient's profile
        else:  # The form is invalid
            return redirect('edit-profile')  # Redirect to the edit profile page

    context = {  # Context to render the view
        'form': form,  # The form
        'profile': profile,  # The patient's profile
    }
    return render(request, 'pages/user-control/edit-profile.html', context)  # Render the view


def contact_view(request):  # The contact page
    """
    This view will render the contact page.
    :param request:

    This view will render a form to contact the admin panel.
    The feedback will be saved in the database.

    :return: renders the contact page
    """
    
    if request.method == 'POST':  # If the form has been submitted...
        name = request.POST['name']  # Get the name
        email_add = request.POST['email']  # Get the email
        subject = request.POST['subject']  # Get the subject
        message = request.POST['message']  # Get the message

        FeedbackModel.objects.create(name=name, email=email_add, subject=subject, message=message)  # Create a feedback

        messages.success(request, "Feedback sent successfully.")  # Show a success message

        return render(request, 'pages/utils/contact.html')  # Redirect to the contact page

    return render(request, 'pages/utils/contact.html')  # Render the view


@login_required(login_url='login')
def account_settings_view(request):  # The account settings page
    """
    This view will render the account settings page.
    :param request:

    This view will render a form to change the account settings.
    User can change his/her name, email, and password from this page.

    :return: renders the account settings page
    """
    
    user = request.user  # Get the user

    information_form = AccountInformationForm(instance=user)  # A form bound to the user's account information
    password_form = PasswordChangeForm(request.user)  # A form bound to the user's password change
    if request.method == 'POST':  # If the form has been submitted...
        information_form = AccountInformationForm(request.POST, instance=user)  # A form bound to the POST data
        password_form = PasswordChangeForm(request.user, request.POST)  # A form bound to the POST data

        if information_form.is_valid():  # All validation rules pass
            information_form.save()  # Save the form
            user.save()  # Save the user
            return redirect('account-settings')  # Redirect to the account settings page

        elif password_form.is_valid():  # All validation rules pass
            user = password_form.save()  # Save the user
            update_session_auth_hash(request, user)  # Update the session with the new password
            messages.success(request, 'Your password was successfully updated!')  # Show a success message
            return redirect('account-settings')  # Redirect to the account settings page
        else:  # The form is invalid
            context = {  # Context to render the view
                'information_form': information_form,  # The form
                'password_form': password_form,  # The form
            }
            return render(request, 'pages/user-control/account-settings.html', context)  # Render the view
    context = {  # Context to render the view
        'information_form': information_form,  # The form
        'password_form': password_form,  # The form
    }
    return render(request, 'pages/user-control/account-settings.html', context)  # Render the view
