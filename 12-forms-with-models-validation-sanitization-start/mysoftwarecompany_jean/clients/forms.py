from django import forms
from .models import Company, Role


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class NewsletterSignupForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "email", "website", "description", "phone_number"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        if len(name) < 3:
            raise forms.ValidationError("Company name must be at least 3 characters long.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        if len(description) < 30:
            raise forms.ValidationError("Description must be at least 30 characters long.")
        return description

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        name = cleaned_data.get("name", "")
        description = cleaned_data.get("description", "")

        # Unique email
        if email and Company.objects.filter(email=email).exists():
            self.add_error("email", "A company with this email already exists.")

        # Forbidden words
        forbidden_words = ["spam", "fake", "scam"]
        for word in forbidden_words:
            if word in name.lower() or word in description.lower():
                raise forms.ValidationError(
                    f"The company contains a forbidden word: {word}"
                )

        # Phone number validation
        phone = cleaned_data.get("phone_number", "")
        digits = [c for c in phone if c.isdigit()]
        if phone and len(digits) != 10:
            self.add_error("phone_number", "Phone number must contain exactly 10 digits.")

        return cleaned_data


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        if len(name) < 4:
            raise forms.ValidationError("Role name must be at least 4 characters long.")
        return name