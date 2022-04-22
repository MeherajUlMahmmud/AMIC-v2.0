from django.shortcuts import render

from pathology_control.models import TestModel


def pathology_home_view(request):
    bookings = TestModel.objects.filter(user=request.user).order_by("--created_at")

    pending_bookings = bookings.filter(status="pending")
    completed_bookings = bookings.filter(status="completed")
    in_progress_bookings = bookings.filter(status="in progress")
    rejected_bookings = bookings.filter(status="rejected")
    context = {
        "pending_bookings": pending_bookings,
        "completed_bookings": completed_bookings,
        "in_progress_bookings": in_progress_bookings,
        "rejected_bookings": rejected_bookings,
    }
    return render(request, "pages/pathology/pathology_home.html", context)


def pathology_post_view(request):
    return render(request, "pages/pathology/pathology_post.html")


def pathology_detail_view(request):
    return render(request, "pages/pathology/pathology_detail.html")


def update_pathology_view(request):
    return render(request, "pages/pathology/update_pathology.html")


def delete_pathology_view(request):
    return render(request, "pages/pathology/delete_pathology.html")
