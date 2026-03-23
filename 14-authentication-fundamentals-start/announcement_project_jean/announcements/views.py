from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Announcement
from .forms import AnnouncementForm

@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, "announcements/announcement_list.html", {"announcements": announcements})

def create_announcement(request):
    # Only teachers can create announcements
    if request.user.role != "teacher":
        return HttpResponseForbidden("You are not allowed to create announcements.")

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
