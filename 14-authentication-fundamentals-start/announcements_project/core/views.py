from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('announcement_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # checked the username and password against the database
            user = authenticate(username=username, password=password)
            # authenticate will return a user object if the username and password are correct
            # otherwise it returns None
            if user is not None:
                login(request, user)
                return redirect('announcement_list')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

