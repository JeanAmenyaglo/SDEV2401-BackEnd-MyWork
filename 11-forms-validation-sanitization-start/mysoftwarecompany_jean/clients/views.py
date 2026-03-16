from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm, NewsletterSignupForm


def contact_us(request):
    if request.method == "GET":
        form = ContactForm()
        return render(request, "clients/contact_us.html", {"form": form})

    elif request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_mail(
                subject=f"New contact us message from {name}",
                message=message,
                from_email=email,
                recipient_list=["some_admin_account@test.com"],
            )

            return render(
                request,
                "clients/contact_us.html",
                {"form": ContactForm(), "success": True},
            )

        return render(request, "clients/contact_us.html", {"form": form})


def newsletter(request):
    if request.method == "GET":
        form = NewsletterSignupForm()
        return render(request, "clients/newsletter_signup.html", {"form": form})

    elif request.method == "POST":
        form = NewsletterSignupForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]

            send_mail(
                subject="Newsletter Signup Confirmation",
                message=f"Hi {name},\n\nThank you for signing up for our newsletter!",
                from_email="no-reply@mysoftwarecompany.com",
                recipient_list=[email],
            )

            return render(
                request,
                "clients/newsletter_signup.html",
                {"form": NewsletterSignupForm(), "success": True},
            )

        return render(request, "clients/newsletter_signup.html", {"form": form})