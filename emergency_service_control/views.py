from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from .forms import BloodRequestForm, PlasmaRequestForm
from .models import BloodRequestModel, PlasmaRequestModel
from user_control.models import UserModel


def blood_donation_home_view(request):  # blood donation home page
    """
    This view is the main page for the blood donation app.
    parms: request

    This view renders the home page for the blood donation app along with the active blood requests.

    returns: render of the page
    """

    blood_requests = BloodRequestModel.objects.filter(is_active=True).order_by('-created_at') # get all active blood requests by date posted on descending order

    paginator = Paginator(blood_requests, 16) # Show 16 requests per page
    page = request.GET.get('page', 1) # get page number from url
    try: 
        blood_requests = paginator.page(page) # get the requested page
    except PageNotAnInteger: # if page is not an integer, deliver first page
        blood_requests = paginator.page(1)
    except EmptyPage: # if page is out of range, deliver last page of results
        blood_requests = paginator.page(paginator.num_pages)

    context = { # context to pass to template
        'blood_requests': blood_requests,
    }
    return render(request, "pages/emergency/blood-donation/blood-donation-home.html",
                  context) # render the page to see all the requests


def post_blood_request_view(request):  # post blood request
    """
    This view is the main page for the blood donation app.
    parms: request

    This view renders a form for the user to post a request for blood.

    returns: render of the page    
    """
    task = "Post New" 
    form = BloodRequestForm() # create a blank form

    if request.method == 'POST': # if the form has been submitted
        form = BloodRequestForm(request.POST) # create a form from the submitted data
        if form.is_valid(): # check if the form is valid
            blood_request = form.save(commit=False) # create a new blood request
            blood_request.user = request.user # set the user to the current logged in user
            blood_request.save() # save the blood request
            return redirect('blood-donation-home') # redirect to the home page

    context = { # context to pass to template
        'task': task,
        'form': form,
    }
    return render(request,
                  'pages/emergency/blood-donation/blood-donation-create-update-request.html',
                  context)


def blood_request_detail_view(request, pk):  # blood request detail page
    """
    This view will show the details of a specific blood request.
    parms: request, user id
    returns: render of the page

    This view will show the details of a specific blood request, and functionality to activate or deactivate the request.

    It will also show a map of the address where the blood is needed.
    """
    post = BloodRequestModel.objects.get(id=pk) # get the blood request
    print(post.is_active)

    my_post = False # set to false to show that this is not my post
    if request.user.is_authenticated and post.user == request.user: # if the user is logged in and the user who posted the request is the logged in user
        my_post = True # set to true to show that this is my post

    location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q=" # create a link to the google maps page with the latitude and longitude of the request

    if post.location is not None: # if the location is not null
        locations = post.location.split(' ') # split the location into latitude and longitude
        location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q=" 

        for location in locations:
            location_link += location + "%20"

        location_link += "&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed" #

    if request.GET.get('disable_req'): # if the user has clicked the disable request button
        post.is_active = False # set the is_active to false
        post.save() # save the post
        return redirect('blood-donation-request-detail', post.id) # redirect to the request detail page

    if request.GET.get('activate_req'): # if the user has clicked the activate request button
        post.is_active = True # set the is_active to true
        post.save() # save the post
        return redirect('blood-donation-request-detail', post.id) # redirect to the request detail page

    context = { # context to pass to template
        'post': post,
        'my_post': my_post,
        'location_link': location_link
    }
    return render(request,
                  'pages/emergency/blood-donation/blood-donation-request-details.html',
                  context)


def update_blood_request_view(request, pk):  # update blood request
    """
    This view will show the details of a specific blood request.
    parms: request, user id
    returns: render of the page

    This view will show a form for the user to update a specific blood request.
    """
    task = "Update"
    post = BloodRequestModel.objects.get(id=pk) # get the blood request
    form = BloodRequestForm(instance=post) # create a blank form
    if request.method == 'POST': # if the form has been submitted
        form = BloodRequestForm(request.POST, instance=post) # create a form from the submitted data
        if form.is_valid(): # check if the form is valid
            form.save() # save the form
            return redirect('blood-donation-request-detail', post.id) # redirect to the request detail page
        else: # if the form is not valid
            return redirect('blood-donation-update-request', post.id) # redirect to the request update page
    context = {
        'task': task,
        'post': post,
        'form': form,
    }
    return render(request,
                  'pages/emergency/blood-donation/blood-donation-create-update-request.html',
                  context)


def delete_blood_request_view(request, pk):  # delete blood request
    """
    This view will delete a specific blood request.
    parms: request, user id
    returns: redirect to the request list page

    This view will delete a specific blood request.
    """
    post = BloodRequestModel.objects.get(id=pk) # get the blood request
    if request.method == 'POST': # if the form has been submitted
        post.delete() # delete the blood request
        return redirect('users-requests', post.user.id) # redirect to the user's requests page

    context = {
        'post': post,
    }
    return render(request,
                  'pages/emergency/blood-donation/blood-donation-request-delete.html',
                  context)


def users_requests_view(request, pk):  # users requests page
    """
    This view will show all the blood requests for a user.
    parms: request, user id
    returns: render of the page

    This view will show all the blood requests for a specific user.
    """
    user = UserModel.objects.get(id=pk) # get the user
    blood_requests = BloodRequestModel.objects.filter(user=user).order_by('-created_at') # get all the blood requests of the user by order of posted date on descending order

    paginator = Paginator(blood_requests, 16) # show 16 requests per page
    page = request.GET.get('page', 1) # get the page number

    try:
        blood_requests = paginator.page(page) # get the requested page
    except PageNotAnInteger: # if page is not an integer, deliver first page
        blood_requests = paginator.page(1)
    except EmptyPage: # if page is out of range, deliver last page of results
        blood_requests = paginator.page(paginator.num_pages)

    context = {
        'user': user,
        'blood_requests': blood_requests,
    }
    return render(request, 'pages/emergency/blood-donation/user-requests.html', context)


def plasma_donation_home_view(request):
    """
    This view is the main page for the plasma donation app.
    parms: request

    This view renders the home page for the plasma donation app along with the active plasma requests.

    returns: render of the page
    """
    plasma_requests = PlasmaRequestModel.objects.filter(is_active=True).order_by('-created_at')  # Get all active plasma requests order by date on descending order

    # Show 16 plasma requests per page
    paginator = Paginator(plasma_requests, 16)
    page = request.GET.get('page', 1)  # Get the page number to display
    try:
        # Get the plasma requests for the page
        plasma_requests = paginator.page(page)
    except PageNotAnInteger:  # If page is not an integer, deliver first page.
        plasma_requests = paginator.page(1)
    except EmptyPage:  # If page is out of range, deliver last page of results.
        plasma_requests = paginator.page(paginator.num_pages)

    context = {  # Context for the page
        'plasma_requests': plasma_requests,
    }
    return render(request, "pages/emergency/plasma-donation/plasma-donation-home.html",
                  context)  # render a page with a list of all the plasma requests


@login_required(login_url='login')
def post_plasma_request_view(request):
    """
    This view is the main page for the plasma donation app.
    parms: request

    This view renders a form for the user to post a request for plasma.

    returns: render of the page    
    """
    task = "Post New"
    form = PlasmaRequestForm()  # An empty form for POST request

    if request.method == 'POST':  # If the form has been submitted...
        form = PlasmaRequestForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Create a new plasma request
            blood_request = form.save(commit=False)
            blood_request.user = request.user  # Set the user
            blood_request.save()  # Save the plasma request
            return redirect('plasma-donation-home')  # Redirect to home page

    context = {
        'task': task,
        'form': form,
    }
    return render(request,
                  'pages/emergency/plasma-donation/plasma-donation-create-update-request.html',
                  context)  # render a page with the form to post a request for plasma


def plasma_request_detail_view(request, pk):
    """
    This view will show the details of a specific plasma request.
    parms: request, user id
    returns: render of the page

    This view will show the details of a specific plasma request, and functionality to activate or deactivate the request.

    It will also show a map of the address where the plasma is needed.
    """
    post = PlasmaRequestModel.objects.get(id=pk) # Get the request

    my_post = False # Flag to check if the user is the owner of the request
    if request.user.is_authenticated and post.user == request.user: # If the user is logged in and the user is the owner of the request
        my_post = True # Set the flag

    location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

    if post.location is not None: # If the request has a location
        locations = post.location.split(' ') # Split the location string into a list
        location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

        for location in locations:
            location_link += location + "%20"

        location_link += "&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"

    if request.GET.get('disable_req'): # If the request is disabled
        post.is_active = False # Set the flag to false
        post.save() # Save the flag
        return redirect('plasma-donation-request-detail', post.id) # Redirect to the request detail page

    if request.GET.get('activate_req'): # If the request is active
        post.is_active = True # Set the flag to true
        post.save() # Save the flag
        return redirect('plasma-donation-request-detail', post.id) # Redirect to the request detail page

    context = { # Context for the page
        'post': post,
        'my_post': my_post,
        'location_link': location_link
    }
    return render(request,
                  'pages/emergency/plasma-donation/plasma-donation-request-details.html',
                  context) # render a page with the request details


@login_required(login_url='login') # Only logged in users should access this
def update_plasma_request_view(request, pk):
    """
    This view will show the details of a specific plasma request.
    parms: request, user id
    returns: render of the page

    This view will show a form for the user to update a specific plasma request.
    """
    task = "Update"
    post = PlasmaRequestModel.objects.get(id=pk) # Get the request
    form = PlasmaRequestForm(instance=post) # An empty form
    if request.method == 'POST': # If the form has been submitted...
        form = PlasmaRequestForm(request.POST, instance=post) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save() # Save the plasma request
            return redirect('plasma-donation-request-detail', post.id) # Redirect to the detail page for the request
        else: # If the form is not valid
            return redirect('plasma-donation-update-request', post.id) # Redirect to the update page for the request
    context = { # Context for the page
        'task': task,
        'post': post,
        'form': form,
    }
    return render(request,
                  'pages/emergency/plasma-donation/plasma-donation-create-update-request.html',
                  context) # render a page with the form to update a request for plasma


@login_required(login_url='login') # Only logged in users should access this
def delete_plasma_request_view(request, pk):
    """
    This view will delete a specific plasma request.
    parms: request, user id
    returns: redirect to the request list page

    This view will delete a specific plasma request.
    """
    post = PlasmaRequestModel.objects.get(id=pk) # Get the request
    if request.method == 'POST': # If the form has been submitted...
        post.delete() # Delete the request
        return redirect('users-plasma-requests', post.user.id) # Redirect to the user page

    context = { # Context for the page
        'post': post,
    }
    return render(request,
                  'pages/emergency/plasma-donation/plasma-donation-request-delete.html',
                  context) # render a page to delete the plasma requests


def users_requests_view(request, pk):
    """
    This view will show all the plasma requests for a user.
    parms: request, user id
    returns: render of the page

    This view will show all the plasma requests for a specific user.
    """
    user = UserModel.objects.get(id=pk) # Get the user
    plasma_requests = PlasmaRequestModel.objects.filter(user=user).order_by('-created_at')  # Get all plasma requests for a user

    paginator = Paginator(plasma_requests, 16) # Show 16 requests per page
    page = request.GET.get('page', 1) # Get the page number to display

    try:
        plasma_requests = paginator.page(page) # Get the page
    except PageNotAnInteger: # If page is not an integer, deliver first page.
        plasma_requests = paginator.page(1)
    except EmptyPage: # If page is out of range, deliver last page of results
        plasma_requests = paginator.page(paginator.num_pages)

    context = { # Context to render the page
        'user': user,
        'plasma_requests': plasma_requests,
    }
    return render(request, 'pages/emergency/plasma-donation/user-plasma-requests.html', context) # render the page

