from django.shortcuts import render, redirect
# import login_required decorator
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

# Create your views here.
from .models import Announcement
from .forms import AnnouncementForm

def is_teacher(user):
    return user.role == 'teacher'

@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(
        request,
        'announcements/announcement_list.html',
        {'announcements': announcements}
    )

@login_required
#@user_passes_test(is_teacher, login_url='login')  # only allow teachers to access this view
@permission_required('announcements.add_announcement', raise_exception=True)  # only allow users with add_announcement permission to access this view
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            # the commit false allows us to modify the announcement object before saving it to the database
            announcement.created_by = request.user
            announcement.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/create_announcement.html', {'form': form})