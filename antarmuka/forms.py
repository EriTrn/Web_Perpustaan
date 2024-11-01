from django import forms
from .models import Antarmuka

# Create your models here.

class AntarmukaForm(forms.ModelForm):
    class Meta:
        model = Antarmuka
        fields = ['judul', 'image', 'konten']


# Contact us form
class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='Full Name')
    email = forms.EmailField(max_length=200, label='Email')
    message = forms.CharField(widget=forms.Textarea, label='Message')