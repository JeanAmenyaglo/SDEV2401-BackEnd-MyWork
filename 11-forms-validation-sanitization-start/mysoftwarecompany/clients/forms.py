from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Full Name")
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    # Custom Validation 
    # the clean_<fieldname> method is used to add custom validation to a single field
    def clean_name(self):
        name = self.cleaned_data['name']
        # if using .get('name') add name to the if statement to make sure 'None' wasn't returned
        #   if name and len(name) < 2
        if len(name) < 2:
            # this will raise a validation error if the name is less than 2 characters long
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message