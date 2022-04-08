from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.utils.text import slugify

from user_control.models import UserModel
from .forms import *


def community_home_view(request):
    """
    This view is the home page for the patient community.
    params: request - the request object
    returns render the patient community home page

    This view will show all the community posts.
    """
    posts = CommunityPostModel.objects.all() # Get all posts

    is_patient = False # Set the flag to false
    if request.user.is_authenticated and request.user.is_patient: # If user is authenticated and is a patient, set the flag to true
        is_patient = True # Set the flag to true

    paginator = Paginator(posts, 5) # Show 5 posts per page
    page = request.GET.get('page', 1) # Get the page number
    try:
        posts = paginator.page(page) # Get the page
    except PageNotAnInteger: # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage: # If page is out of range, deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    context = { # Pass the variables to the template
        'posts': posts,
        'latest_posts': posts[:3], # Get the latest 3 posts
        'is_patient': is_patient,
    }
    return render(request, "pages/patient-community/community-home.html", context)


def community_post_create_view(request):
    """
    This view is the create post page for the patient community.
    params: request - the request object
    returns render the patient community create post page

    This view will show the form to create a new post.
    """
    task = "Create New"
    form = AddEditPostForm() # An unbound form

    if request.method == 'POST': # If the form has been submitted...
        form = AddEditPostForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            post = form.save(commit=False) # Create a new object from the form, but don't save it to the database
            post.author = request.user # Set the author to the current user
            post.save() # Save the object to the database
            slug_str = "%s %s" % (post.title, post.created_at) # Create a slug from the title and date
            post.slug = slugify(slug_str) # Create the slug
            post.save() # Save the object to the database
            return redirect('community-home') # Redirect to the home page

    context = { # Pass the variables to the template
        'task': task,
        'form': form,
    }
    return render(request,
                  'pages/patient-community/community-create-update-post.html',
                  context) # render the patient community create post page


def community_post_detail_view(request, slug):
    """
    This view is the detail page for the patient community.
    params: request - the request object
    returns render the patient community detail page

    This view will show the detail page for a post.
    It will also allow the user to update and delete the post.
    """
    post = CommunityPostModel.objects.get(slug=slug) # Get the post
    posts = CommunityPostModel.objects.all()[:3] # Get the latest 3 posts
    author = UserModel.objects.get(id=post.author.id) # Get the author

    my_article = False # Set the flag to false
    if request.user == post.author: # If the user is the author, set the flag to true
        my_article = True # Set the flag to true

    context = { # Pass the variables to the template
        'post': post,
        'latest_posts': posts,
        'author': author,
        'my_article': my_article,
    }
    return render(request,
                  'pages/patient-community/community-post-details.html',
                  context) # render the patient community detail page


def community_post_update_view(request, slug):
    """
    This view is the update page for the patient community.
    params: request - the request object
    returns render the patient community update page

    This view will show the form to update a post.
    """
    task = "Update"
    post = CommunityPostModel.objects.get(slug=slug) # Get the post

    form = AddEditPostForm(instance=post) # An unbound form
    if request.method == 'POST': # If the form has been submitted...
        form = AddEditPostForm(request.POST, request.FILES, instance=post) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            post = form.save() # Save the object to the database
            slug_str = "%s %s" % (post.title, post.created_at) # Create a slug from the title and date
            post.slug = slugify(slug_str) # Create the slug
            post.save() # Save the object to the database
            return redirect('community-post-detail', slug=post.slug) # Redirect to the detail page

    context = { # Pass the variables to the template
        'task': task,
        'post': post,
        'form': form,
    }
    return render(request,
                  'pages/patient-community/community-create-update-post.html',
                  context) # render the patient community update page


def community_post_delete_view(request, slug):
    """
    This view is the delete page for the patient community.
    params: request - the request object
    returns render the patient community delete page

    This view will show the form to delete a post.
    """
    post = CommunityPostModel.objects.get(slug=slug) # Get the post

    if request.method == 'POST': # If the form has been submitted...
        post.delete() # Delete the object from the database
        return redirect('community-home') # Redirect to the home page

    context = {'post': post} # Pass the variables to the template
    return render(request,
                  'pages/patient-community/community-delete-post.html',
                  context) # render the patient community delete page
