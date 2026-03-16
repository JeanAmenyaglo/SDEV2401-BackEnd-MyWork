from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from .forms import (
    ContactForm,
    NewsletterSignupForm,
    CompanyForm,
    RoleForm,
)
from .models import Company, Role


def contact_us(request):
    if request.method == "GET":
        form = ContactForm()
        return render(request, "clients/contact_us.html", {"form": form})

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


def create_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            company = form.instance
            return render(
                request,
                "clients/create_company.html",
                {"form": CompanyForm(), "new_company": company},
            )
        return render(request, "clients/create_company.html", {"form": form})

    form = CompanyForm()
    return render(request, "clients/create_company.html", {"form": form})


def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    return render(request, "clients/company_detail.html", {"company": company})


def create_role(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            return render(
                request,
                "clients/create_role.html",
                {"form": RoleForm(), "new_role": role},
            )
        return render(request, "clients/create_role.html", {"form": form})

    form = RoleForm()
    return render(request, "clients/create_role.html", {"form": form})