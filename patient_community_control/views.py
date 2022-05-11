from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.text import slugify

from user_control.models import UserModel
from .forms import *


@login_required(login_url="login")
def community_home_view(request):
    posts = CommunityPostModel.objects.all()

    is_patient = False
    if request.user.is_authenticated and request.user.is_patient:
        is_patient = True

    paginator = Paginator(posts, 5)
    page = request.GET.get("page", 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
        "latest_posts": posts[:3],
        "is_patient": is_patient,
    }
    return render(request, "pages/patient-community/community-home.html", context)


@login_required(login_url="login")
def community_post_create_view(request):
    task = "Create New"
    form = AddEditPostForm()

    if request.method == "POST":
        form = AddEditPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            slug_str = "%s %s" % (post.title, post.created_at)
            post.slug = slugify(slug_str)
            post.save()
            return redirect("community-home")

    context = {
        "task": task,
        "form": form,
    }
    return render(
        request, "pages/patient-community/community-create-update-post.html", context
    )


@login_required(login_url="login")
def community_post_detail_view(request, slug):
    post = CommunityPostModel.objects.get(slug=slug)
    posts = CommunityPostModel.objects.all()[:3]
    author = UserModel.objects.get(id=post.author.id)

    my_article = False
    if request.user == post.author:
        my_article = True

    context = {
        "post": post,
        "latest_posts": posts,
        "author": author,
        "my_article": my_article,
    }
    return render(
        request, "pages/patient-community/community-post-details.html", context
    )


def community_post_update_view(request, slug):
    task = "Update"
    post = CommunityPostModel.objects.get(slug=slug)

    form = AddEditPostForm(instance=post)
    if request.method == "POST":
        form = AddEditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            slug_str = "%s %s" % (
                post.title,
                post.created_at,
            )
            post.slug = slugify(slug_str)
            post.save()
            return redirect("community-post-detail", slug=post.slug)

    context = {
        "task": task,
        "post": post,
        "form": form,
    }
    return render(
        request, "pages/patient-community/community-create-update-post.html", context
    )


def community_post_delete_view(request, slug):
    post = CommunityPostModel.objects.get(slug=slug)

    if request.method == "POST":
        post.delete()
        return redirect("community-home")

    context = {"post": post}
    return render(
        request, "pages/patient-community/community-delete-post.html", context
    )
