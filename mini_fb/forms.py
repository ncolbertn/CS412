from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['first_name', 'surname', 'city', 'email', 'pfp']

class CreateStatusMessageForm(forms.ModelForm):

    class Meta:
        model = StatusMessage
        fields = ['message']