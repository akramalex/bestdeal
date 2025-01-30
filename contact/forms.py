from django import forms
from .models import ContactMessage

""" ContactForm is a ModelForm for the Contact model,
allowing users to submit their name, email, and message through a form."""


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']