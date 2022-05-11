from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

from .forms import AddEditPostForm
from .models import AdviceModel


@login_required(login_url="login")
def advisor_home_view(request):
    post_search = request.GET.get('q') # get the search term from the GET request

    if post_search is not None: # if there is a search term, perform a search
        posts = AdviceModel.objects.filter(Q(title__icontains=post_search)).order_by('-created_at') # filter the posts by the search term
    else: # if there is no search term, show all posts
        posts = AdviceModel.objects.order_by('-created_at') # order the posts by date

    paginator = Paginator(posts, 5) # paginate the posts by 5
    page = request.GET.get('page', 1) # get the page number from the GET request
    try:
        posts = paginator.page(page) # get the requested page
    except PageNotAnInteger: # if the requested page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage: # if the requested page is out of range, deliver the last page of results
        posts = paginator.page(paginator.num_pages)

    context = { # create a dictionary to pass to the template engine as its context
        'posts': posts,
        'latest_posts': posts[:3],
        'post_search': post_search
    }
    return render(request, "pages/health-advisor/advisor-home.html",
                  context) # render the response and return it to the client


@login_required(login_url='login') # decorator to ensure that only logged in users can access this view
def advisor_post_create_view(request):
    task = "Create New"
    form = AddEditPostForm() # create an instance of the AddEditPostForm class

    if request.method == 'POST': # if the form has been submitted...
        form = AddEditPostForm(request.POST, request.FILES) # create an instance of the AddEditPostForm class
        if form.is_valid(): # check whether it's valid
            new_post = form.save(commit=False) # create a new post object but don't save it yet
            new_post.author = request.user # set the post's author
            new_post.slug = slugify(new_post.title) # set the post's slug
            new_post.save() # save the post to the database
            form.save() # save the form data to the database
            return redirect('advisor-home') # redirect to the home page

    context = { # create a dictionary to pass to the template engine as its context
        'task': task,
        'form': form,
    }
    return render(request,
                  'pages/health-advisor/advisor-create-update-post.html',
                  context) # render the response and return it to the client


@login_required(login_url='login') # decorator to ensure that only logged in users can access this view
def advisor_post_detail_view(request, slug):
    """
    View a specific post

    :param request: The HTTP request
    :param slug: the slug of the post to view
    :return: The response for the request

    This view will display the details of a post and allow the user to edit the post.
    """
    post_search = request.GET.get('q') # get the search term from the GET request

    if post_search is not None: # if there is a search term, perform a search
        posts = AdviceModel.objects.filter(Q(title__icontains=post_search)).order_by('-created_at') # filter the posts by the search term
        context = { # create a dictionary to pass to the template engine as its context
            'posts': posts,
            'latest_posts': posts[:3],
            'post_search': post_search
        }
        return render(request, "pages/health-advisor/advisor-home.html",
                      context) # render the response and return it to the client

    latest_posts = AdviceModel.objects.order_by('-created_at')[:3] # order the posts by date
    post = AdviceModel.objects.get(slug=slug) # get the post object

    my_post = False # set the flag to false
    if request.user == post.author: # if the user is the post's author...
        my_post = True # set the flag to true

    context = { # create a dictionary to pass to the template engine as its context
        'post': post,
        'my_post': my_post,
        'latest_posts': latest_posts,
        'post_search': post_search
    }
    return render(request, 'pages/health-advisor/advisor-post-details.html', context) # render the response and return it to the client


@login_required(login_url='login') # decorator to ensure that only logged in users can access this view
def advisor_post_update_view(request, slug):
    """
    This view will update a post
    :param request: The HTTP request
    :param slug: the slug of the post to update
    :return: The response for the request

    This view will update a post and return the user to the page containing the updated post.
    """
    task = "Update"
    post = AdviceModel.objects.get(slug=slug) # get the post object
    form = AddEditPostForm(instance=post) # create an instance of the AddEditPostForm class
    if request.method == 'POST': # if the form has been submitted...
        form = AddEditPostForm(request.POST, request.FILES, instance=post) # create an instance of the AddEditPostForm class
        if form.is_valid(): # check whether it's valid
            post = form.save() # save the post to the database
            post.slug = slugify(post.title) # set the post's slug
            form.save() # save the form data to the database
            return redirect('advisor-post-detail', post.slug) # redirect to the post detail page
        else: # if the form is not valid, return the form to the user
            return redirect('advisor-post-update', post.slug) # redirect to the post update page

    context = { # create a dictionary to pass to the template engine as its context
        'task': task,
        'form': form,
        'post': post,
    }
    return render(request, 'pages/health-advisor/advisor-create-update-post.html', context) # render the response and return it to the client


@login_required(login_url='login') # decorator to ensure that only logged in users can access this view
def advisor_post_delete_view(request, slug):
    post = AdviceModel.objects.get(slug=slug) # get the post object
    if request.method == 'POST': # if the form has been submitted...
        post.delete() # delete the post
        return redirect('advisor-home') # redirect to the home page

    context = { # create a dictionary to pass to the template engine as its context
        'post': post,
    }
    return render(request, 'pages/health-advisor/advisor-delete-post.html', context) # render the response and return it to the client
