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
    articles = ArticleModel.objects.order_by("?")

    is_doctor = False
    if request.user.is_authenticated and request.user.is_doctor:
        is_doctor = True

    paginator = Paginator(articles, 5)
    page = request.GET.get("page", 1)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    categories = get_categories()
    context = {
        "articles": articles,
        "latest_articles": articles[:3],
        "is_doctor": is_doctor,
        # 'blog_search': blog_search,
        "categories": categories,
    }
    return render(request, "pages/article/article-home.html", context)


def article_details_view(request, slug):
    latest_articles = ArticleModel.objects.order_by("-created_at")[:3]
    article = ArticleModel.objects.get(slug=slug)

    my_article = False
    if request.user == article.author:
        my_article = True

    author = UserModel.objects.get(id=article.author.id)
    author_profile = DoctorModel.objects.get(user=author)

    categories = get_categories()

    context = {
        "article": article,
        "my_article": my_article,
        "latest_articles": latest_articles,
        "author": author,
        "author_profile": author_profile,
        "categories": categories,
    }
    return render(request, "pages/article/article-details.html", context)


@login_required(login_url="login")
@show_to_doctor(allowed_roles=["is_doctor"])
def post_article_view(request):
    task = "Post New"
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            slug_str = "%s %s" % (article.title, article.created_at)
            article.slug = slugify(slug_str)
            article.save()
            return redirect("article-home")
        else:
            context = {
                "task": task,
                "form": form,
            }
            return render(request, "pages/article/add-edit-article.html", context)

    context = {
        "task": task,
        "form": form,
    }
    return render(request, "pages/article/add-edit-article.html", context)


@login_required(login_url="login")
@show_to_doctor(allowed_roles=["is_doctor"])
def edit_article_view(request, slug):
    task = "Update"
    article = ArticleModel.objects.get(slug=slug)
    form = ArticleForm(instance=article)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save()
            slug_str = "%s %s" % (article.title, article.created_at)
            article.slug = slugify(slug_str)
            form.save()
            return redirect("article-details", article.slug)
        else:
            return redirect("edit-article", article.slug)

    context = {
        "task": task,
        "form": form,
        "article": article,
    }
    return render(request, "pages/article/add-edit-article.html", context)


@login_required(login_url="login")
@show_to_doctor(allowed_roles=["is_doctor"])
def delete_article_view(request, slug):
    article = ArticleModel.objects.get(slug=slug)
    if request.method == "POST":
        article.delete()
        return redirect("users-articles", request.user.id)

    context = {
        "article": article,
    }
    return render(request, "pages/article/delete-article.html", context)


def users_articles_view(request, pk):
    user = UserModel.objects.get(id=pk)
    latest_articles = ArticleModel.objects.order_by("-created_at")[:3]
    articles = ArticleModel.objects.filter(author=user).order_by("-created_at")

    is_doctor = False
    if request.user.is_authenticated and request.user.is_doctor:
        is_doctor = True

    paginator = Paginator(articles, 5)
    page = request.GET.get("page", 1)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    categories = get_categories()
    context = {
        "user": user,
        "articles": articles,
        "latest_articles": latest_articles,
        # 'blog_search': blog_search,
        "is_doctor": is_doctor,
        "categories": categories,
    }
    return render(request, "pages/article/user-articles.html", context)


def category_articles_view(request, cat):
    latest_articles = ArticleModel.objects.order_by("-created_at")[:3]
    cat_articles = ArticleModel.objects.filter(category__category=cat).order_by(
        "-created_at"
    )

    is_doctor = False
    if request.user.is_authenticated and request.user.is_doctor:
        is_doctor = True

    paginator = Paginator(cat_articles, 5)
    page = request.GET.get("page", 1)
    try:
        cat_articles = paginator.page(page)
    except PageNotAnInteger:
        cat_articles = paginator.page(1)
    except EmptyPage:
        cat_articles = paginator.page(paginator.num_pages)

    categories = get_categories()
    context = {
        "articles": cat_articles,
        "cat": cat,
        "latest_articles": latest_articles,
        "is_doctor": is_doctor,
        "categories": categories,
    }
    return render(request, "pages/article/category-article.html", context)
