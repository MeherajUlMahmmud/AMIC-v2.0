from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from .forms import *
from .models import *
from .utils import *
from user_control.models import *
from user_control.decorators import show_to_doctor


def article_home_view(request):
    """
    This view is for the home page of the blog.
    params: request - the request object
    returns: render - the render home page for articles

    This view fetches all the articles from database andrenders on the home page.
    """
    articles = ArticleModel.objects.order_by('-created_at') # get all articles
    
    is_doctor = False # set is_doctor to false
    if request.user.is_authenticated and request.user.is_doctor: # if user is logged in and is a doctor
        is_doctor = True # set is_doctor to true if user is doctor

    paginator = Paginator(articles, 5) # set paginator to 5 articles per page
    page = request.GET.get('page', 1) # get page from request
    try:
        articles = paginator.page(page) # get articles from paginator
    except PageNotAnInteger: # if page is not an integer
        articles = paginator.page(1)
    except EmptyPage: # if page is out of range
        articles = paginator.page(paginator.num_pages)

    categories = get_categories() # get categories
    context = { # Context to pass to the template
        'articles': articles,
        'latest_articles': articles[:3],
        'is_doctor': is_doctor,
        # 'blog_search': blog_search,
        'categories': categories,
    }
    return render(request, 'pages/article/article-home.html', context) # render home page


def article_details_view(request, slug):
    """
    This view is for the article details page.

    params: request - the request object
    returns: render - the render article details page

    This view fetches a specific article from database and renders on the article details page.
    
    """
    latest_articles = ArticleModel.objects.order_by('-created_at')[:3] # get latest 3 articles
    article = ArticleModel.objects.get(slug=slug) # get article

    my_article = False # set my_article to false
    if request.user == article.author: # if user is the author of the article
        my_article = True # set my_article to true if user is the author of the article

    author = UserModel.objects.get(id=article.author.id) # get author of the article
    author_profile = DoctorModel.objects.get(user=author) # get author's profile

    categories = get_categories() # get categories

    context = { # Context to pass to the template
        'article': article,
        'my_article': my_article,
        'latest_articles': latest_articles,
        'author': author,
        'author_profile': author_profile,
        'categories': categories,
    }
    return render(request, 'pages/article/article-details.html', context)


@login_required(login_url='login') # this decorator will prevent a user from accessing this view if they are not logged in
@show_to_doctor(allowed_roles=['is_doctor']) # this decorator will prevent a user from accessing this view if they are not a doctor
def post_article_view(request):
    """
    This view is for the post article page.

    params: request - the request object
    returns: render - the render post article page

    This view renders a form to post an article. This view also checks if the user is a doctor and if the user is a doctor, they can post an article.
    """
    task = "Post New"
    form = ArticleForm() # instantiate the form
    if request.method == 'POST': # if the request method is POST
        form = ArticleForm(request.POST, request.FILES) # instantiate the form with the POST data
        if form.is_valid(): # if the form is valid
            article = form.save(commit=False) # save the form
            article.author = request.user # set article author to current user
            article.save() # save the article
            slug_str = "%s %s" % (article.title, article.created_at) # create slug
            article.slug = slugify(slug_str) # add slug to article
            article.save() # save the article
            return redirect('article-home') # redirect to article home page
        else: # if the form is not valid
            context = { # Context to pass to the template
                'task': task,
                'form': form,
            }
            return render(request, 'pages/article/add-edit-article.html', context) # render the form

    context = {
        'task': task,
        'form': form,
    }
    return render(request, 'pages/article/add-edit-article.html', context)


@login_required(login_url='login') # this decorator will prevent a user from accessing this view if they are not logged in
@show_to_doctor(allowed_roles=['is_doctor']) # this decorator will prevent a user from accessing this view if they are not a doctor
def edit_article_view(request, slug):
    """
    This view is for the edit article page.

    params: request - the request object
    returns: render - the render edit article page

    This view renders a form to edit an article. This view also checks if the user is a doctor and if the user is a doctor, they can edit an article.
    """
    task = "Update"
    article = ArticleModel.objects.get(slug=slug) # get article
    form = ArticleForm(instance=article) # instantiate the form
    if request.method == 'POST': # if the request method is POST
        form = ArticleForm(request.POST, request.FILES, instance=article) # instantiate the form with the POST data
        if form.is_valid(): # if the form is valid
            article = form.save() # save the form
            slug_str = "%s %s" % (article.title, article.created_at) # create slug
            article.slug = slugify(slug_str) # add slug to article
            form.save() # save the article
            return redirect('article-details', article.slug) # redirect to article details page
        else: # if the form is not valid
            return redirect('edit-article', article.slug) # redirect to edit article page

    context = { # Context to pass to the template
        'task': task,
        'form': form,
        'article': article
    }
    return render(request, 'pages/article/add-edit-article.html', context)


@login_required(login_url='login')
@show_to_doctor(allowed_roles=['is_doctor'])
def delete_article_view(request, slug):
    """
    This view is for the delete article page.

    params: request - the request object
    returns: render - the render delete article page

    This view renders a page to delete an article. This view also checks if the user is a doctor and if the user is a doctor, and author of the article, they can delete an article.
    """
    article = ArticleModel.objects.get(slug=slug) # get article
    if request.method == 'POST': # if the request method is POST
        article.delete() # delete the article
        return redirect('users-articles', request.user.id) # redirect to user's articles page

    context = { # Context to pass to the template
        'article': article,
    }
    return render(request, 'pages/article/delete-article.html', context)


def users_articles_view(request, pk):
    """
    This view is for the users articles page.

    params: request - the request object
    returns: render - the render users articles page

    This view renders a page with all the articles written by the user.
    """
    user = UserModel.objects.get(id=pk) # get user
    latest_articles = ArticleModel.objects.order_by('-created_at')[:3] # get latest 3 articles
    articles = ArticleModel.objects.filter(author=user).order_by('-created_at') # get articles by user

    is_doctor = False # set is_doctor to false
    if request.user.is_authenticated and request.user.is_doctor: # if user is authenticated and is a doctor
        is_doctor = True # set is_doctor to true

    paginator = Paginator(articles, 5) # paginate articles
    page = request.GET.get('page', 1) # get page

    try:
        articles = paginator.page(page) # get articles from page
    except PageNotAnInteger: # if page is not an integer
        articles = paginator.page(1)
    except EmptyPage: # if page is out of range
        articles = paginator.page(paginator.num_pages)

    categories = get_categories() # get categories
    context = {
        'user': user,
        'articles': articles,
        'latest_articles': latest_articles,
        # 'blog_search': blog_search,
        'is_doctor': is_doctor,
        'categories': categories,
    }
    return render(request, 'pages/article/user-articles.html', context)


def category_articles_view(request, cat):
    """
    This view is for the category articles page.

    params: request - the request object
    returns: render - the render category articles page

    This view renders a page with all the articles in a certain category.
    """
    latest_articles = ArticleModel.objects.order_by('-created_at')[:3] # get latest 3 articles
    cat_articles = ArticleModel.objects.filter(category__category=cat).order_by('-created_at') # get articles by category

    is_doctor = False # set is_doctor to false
    if request.user.is_authenticated and request.user.is_doctor: # if user is authenticated and is a doctor
        is_doctor = True # set is_doctor to true

    paginator = Paginator(cat_articles, 5) # paginate articles
    page = request.GET.get('page', 1) # get page
    try:
        cat_articles = paginator.page(page) # get articles from page
    except PageNotAnInteger: # if page is not an integer
        cat_articles = paginator.page(1)
    except EmptyPage: # if page is out of range
        cat_articles = paginator.page(paginator.num_pages)

    categories = get_categories() # get categories
    context = { # Context to pass to the template
        'articles': cat_articles,
        'cat': cat,
        'latest_articles': latest_articles,
        'is_doctor': is_doctor,
        'categories': categories,
    }
    return render(request, 'pages/article/category-article.html', context)
