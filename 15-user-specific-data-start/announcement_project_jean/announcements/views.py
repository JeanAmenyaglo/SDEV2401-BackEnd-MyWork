from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Announcement
from .forms import AnnouncementForm


@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, "announcements/announcement_list.html", {"announcements": announcements})


@login_required
@permission_required('announcements.add_announcement', raise_exception=True)
def create_announcement(request):

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            return redirect("announcement_list")
    else:
        form = AnnouncementForm()

    return render(request, "announcements/create_announcement.html", {"form": form})